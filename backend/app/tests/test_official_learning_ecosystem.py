import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Competency, LearningResource, OfficialSource, ResourceCompetencyMapping
from app.core.security import create_access_token
from app.services.providers import (
    PROVIDER_REGISTRY, get_provider, IntegrationMode,
    IGOTKarmayogiProvider, NSSTATPACProvider,
    MoSPIPublicationsProvider, ESankhyikiDatasetsProvider
)
from app.services.sync_service import synchronize_provider, get_all_provider_statuses
from app.services.live_fetcher import is_official_domain

client = TestClient(app)

def test_domain_allowlist_security():
    assert is_official_domain("https://igotkarmayogi.gov.in/course/101") is True
    assert is_official_domain("https://nssta.gov.in/tpac/2024") is True
    assert is_official_domain("https://mospi.gov.in/publication") is True
    assert is_official_domain("https://esankhyiki.mospi.gov.in/macroindicators") is True
    
    # Reject unverified external or malicious domains
    assert is_official_domain("https://unverified-third-party.com/malicious") is False
    assert is_official_domain("http://phishing-site.org/fake-igot") is False

def test_igot_provider_mode_fallback_and_normalization():
    igot_provider = IGOTKarmayogiProvider()
    assert igot_provider.provider_id == "igot_karmayogi"
    
    # Credentials absent -> CURATED_FALLBACK
    assert igot_provider.integration_mode in [IntegrationMode.CURATED_FALLBACK, IntegrationMode.LIVE_API]
    
    items = igot_provider.discover_and_fetch()
    assert len(items) > 0
    top_item = items[0]
    assert top_item.provider == igot_provider.name
    assert "iGOT Karmayogi" in top_item.title
    assert len(top_item.competencies) > 0
    assert top_item.dedup_hash is not None
    assert top_item.internal_resource_key == "igot-course-stat-01"
    # Curated fallback must NOT claim official provider_external_id or Live Official API
    assert top_item.provider_external_id is None
    assert top_item.provenance_type == "Curated Official Metadata"
    assert top_item.mapping_provenance == "Platform Curated Competency Mapping"

def test_nssta_tpac_provider_normalization():
    tpac_provider = NSSTATPACProvider()
    assert tpac_provider.provider_id == "nssta_tpac"
    
    items = tpac_provider.discover_and_fetch()
    assert len(items) > 0
    tpac_item = items[0]
    assert "NSSTA TPAC" in tpac_item.title
    assert tpac_item.publisher_org == "NSSTA / MoSPI"
    assert len(tpac_item.designation_applicability) > 0
    assert tpac_item.internal_resource_key == "nssta-tpac-2024-01"
    assert tpac_item.provider_external_id is None
    assert tpac_item.mapping_provenance == "Platform Curated Competency Mapping"

def test_provenance_and_external_id_authenticity():
    db_session = SessionLocal()
    try:
        synchronize_provider("igot_karmayogi", db_session)
        synchronize_provider("nssta_tpac", db_session)

        # 1. Verify iGOT curated resources
        igot_res = db_session.query(LearningResource).filter(
            LearningResource.source == "iGOT Karmayogi National Learning Portal"
        ).first()
        assert igot_res is not None
        assert igot_res.provenance_type != "Live Official API", "Curated metadata must not be labeled as Live Official API"
        assert igot_res.provenance_type == "Curated Official Metadata"
        assert igot_res.provider_external_id is None, "Internal keys must not be mislabeled as provider external IDs"
        assert igot_res.verification_level in ["PORTAL_VERIFIED", "UNVERIFIED"]

        # 2. Verify mapping provenance
        mapping = db_session.query(ResourceCompetencyMapping).filter(
            ResourceCompetencyMapping.resource_id == igot_res.id
        ).first()
        assert mapping is not None
        assert mapping.mapping_provenance == "Platform Curated Competency Mapping"
    finally:
        db_session.close()

def test_provider_synchronization_deduplication_idempotency():
    db_session = SessionLocal()
    try:
        # First synchronization
        res1 = synchronize_provider("igot_karmayogi", db_session)
        assert res1["status"] == "success"
        ingested_count = res1["items_ingested"]

        initial_total_resources = db_session.query(LearningResource).filter(
            LearningResource.source == "iGOT Karmayogi National Learning Portal"
        ).count()
        assert initial_total_resources >= ingested_count

        # Second synchronization (Idempotent - should NOT duplicate)
        res2 = synchronize_provider("igot_karmayogi", db_session)
        assert res2["status"] == "success"
        assert res2["items_ingested"] == 0
        assert res2["items_updated"] >= ingested_count

        final_total_resources = db_session.query(LearningResource).filter(
            LearningResource.source == "iGOT Karmayogi National Learning Portal"
        ).count()
        assert final_total_resources == initial_total_resources, "Repeated synchronization must not duplicate resources in DB."
    finally:
        db_session.close()

def test_admin_learning_sources_api_rbac():
    db_session = SessionLocal()
    try:
        # 1. Non-admin user
        user = User(
            email=f"regular_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Regular Officer",
            designation="Statistical Officer",
            department="Field Operations Division",
            role="officer"
        )
        db_session.add(user)

        # 2. Admin user
        admin = User(
            email=f"admin_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Admin Officer",
            designation="Director General",
            department="MoSPI Headquarters",
            role="admin"
        )
        db_session.add(admin)
        db_session.commit()

        user_token = create_access_token({"sub": str(user.id)})
        admin_token = create_access_token({"sub": str(admin.id)})

        # Non-admin access attempt -> 403 FORBIDDEN
        res_user = client.get("/api/v1/admin/learning-sources", headers={"Authorization": f"Bearer {user_token}"})
        assert res_user.status_code == 403

        res_user_ref = client.post("/api/v1/admin/learning-sources/igot_karmayogi/refresh", headers={"Authorization": f"Bearer {user_token}"})
        assert res_user_ref.status_code == 403

        # Admin access -> 200 OK
        res_admin = client.get("/api/v1/admin/learning-sources", headers={"Authorization": f"Bearer {admin_token}"})
        assert res_admin.status_code == 200
        data = res_admin.json()
        assert data["status"] == "success"
        assert len(data["providers"]) >= 4

        # Admin refresh -> 200 OK
        res_admin_ref = client.post("/api/v1/admin/learning-sources/nssta_tpac/refresh", headers={"Authorization": f"Bearer {admin_token}"})
        assert res_admin_ref.status_code == 200
        ref_data = res_admin_ref.json()
        assert ref_data["status"] == "success"
        assert ref_data["result"]["provider_id"] == "nssta_tpac"

        # Admin provider status check -> 200 OK
        res_admin_st = client.get("/api/v1/admin/learning-sources/nssta_tpac/status", headers={"Authorization": f"Bearer {admin_token}"})
        assert res_admin_st.status_code == 200
        st_data = res_admin_st.json()
        assert st_data["provider"]["provider_id"] == "nssta_tpac"
        assert "provenance_breakdown" in st_data["provider"]
    finally:
        db_session.close()

def test_multi_provider_recommendation_ranking():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"multi_rec_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Multi Provider Officer",
            designation="Deputy Director (ISS)",
            department="National Accounts Division",
            role="officer"
        )
        db_session.add(user)
        db_session.commit()

        # Synchronize all providers
        synchronize_provider("igot_karmayogi", db_session)
        synchronize_provider("nssta_tpac", db_session)
        synchronize_provider("mospi_publications", db_session)
        synchronize_provider("esankhyiki_datasets", db_session)

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        res = client.get("/api/v1/recommendations/for-you", headers=headers)
        assert res.status_code == 200
        recs = res.json()["recommendations"]
        assert len(recs) > 0

        providers_present = {r["resource"]["publisher_org"] for r in recs}
        assert len(providers_present) >= 1

        for r in recs:
            assert "provenance_type" in r["resource"]
            assert "publisher_org" in r["resource"]
            assert "verification_level" in r["resource"]
            assert "mapping_provenance" in r["resource"]
            assert r["resource"]["mapping_provenance"] == "Platform Curated Competency Mapping"
    finally:
        db_session.close()
