import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Competency, LearningResource, OfficialSource, ResourceCompetencyMapping
from app.core.security import create_access_token
from app.services.source_adapters import ESankhyikiAdapter, compute_resource_dedup_hash
from app.services.official_integration_service import seed_official_sources, refresh_official_sources

client = TestClient(app)

def test_source_validation_and_domain_verification():
    source_info = {
        "source_id": "test_source",
        "name": "Test Source",
        "organization": "MoSPI",
        "base_url": "https://esankhyiki.mospi.gov.in/",
        "source_type": "Official Public Data",
        "access_method": "Downloadable CSV",
        "access_level": "PUBLIC"
    }
    adapter = ESankhyikiAdapter(source_info)

    # Valid official domain item
    valid_item = {
        "title": "Valid MoSPI Dataset",
        "official_url": "https://esankhyiki.mospi.gov.in/macroindicators-main"
    }
    assert adapter.validate_item(valid_item) is True

    # Invalid non-official domain item
    invalid_item = {
        "title": "Malicious Dataset",
        "official_url": "https://unverified-thirdparty-site.com/dataset.csv"
    }
    assert adapter.validate_item(invalid_item) is False

def test_idempotent_official_resource_ingestion():
    db_session = SessionLocal()
    try:
        # Seed official sources
        sources = seed_official_sources(db_session)
        assert len(sources) >= 5

        # First ingestion run
        res1 = refresh_official_sources(db_session)
        assert res1["items_discovered"] > 0
        assert (res1["items_ingested"] + res1["items_updated"]) > 0

        initial_res_count = db_session.query(LearningResource).filter(LearningResource.source_id.isnot(None)).count()
        assert initial_res_count > 0

        # Second ingestion run (idempotency check)
        res2 = refresh_official_sources(db_session)
        assert res2["duplicates_skipped"] >= res1["items_discovered"]

        final_res_count = db_session.query(LearningResource).filter(LearningResource.source_id.isnot(None)).count()
        assert final_res_count == initial_res_count, "Running ingestion twice must not create duplicate resource records"
    finally:
        db_session.close()

def test_competency_mapping_and_provenance_preservation():
    db_session = SessionLocal()
    try:
        refresh_official_sources(db_session)
        macro_res = db_session.query(LearningResource).filter(LearningResource.title.like("%eSankhyiki Macro Indicators%")).first()
        assert macro_res is not None
        assert macro_res.publisher_org == "eSankhyiki"
        assert macro_res.provenance_type in ["Live Official Metadata", "Live Official Data", "Curated Official Metadata"]
        assert macro_res.source_format == "CSV"
        assert macro_res.access_level == "PUBLIC"

        # Check mapping to STAT_NAT_ACC competency
        mappings = db_session.query(ResourceCompetencyMapping).filter(ResourceCompetencyMapping.resource_id == macro_res.id).all()
        assert len(mappings) > 0
        comp_codes = [m.competency.code for m in mappings if m.competency]
        assert "STAT_NAT_ACC" in comp_codes
    finally:
        db_session.close()

def test_restricted_resource_access_level_classification():
    db_session = SessionLocal()
    try:
        refresh_official_sources(db_session)
        unit_res = db_session.query(LearningResource).filter(LearningResource.title.like("%UnitData%")).first()
        assert unit_res is not None
        assert unit_res.access_level in ["REGISTERED", "RESTRICTED"]
        assert unit_res.official_url.startswith("https://www.mospi.gov.in/")
    finally:
        db_session.close()

def test_admin_only_official_sources_endpoints():
    db_session = SessionLocal()
    try:
        # Create regular user
        user_reg = User(
            email=f"reg_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Regular Officer",
            role="user"
        )
        db_session.add(user_reg)
        
        # Create admin user
        user_admin = User(
            email=f"admin_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Admin Officer",
            role="admin"
        )
        db_session.add(user_admin)
        db_session.commit()

        token_reg = create_access_token({"sub": str(user_reg.id)})
        token_admin = create_access_token({"sub": str(user_admin.id)})

        headers_reg = {"Authorization": f"Bearer {token_reg}"}
        headers_admin = {"Authorization": f"Bearer {token_admin}"}

        # Regular user attempt to access admin endpoints -> 403 Forbidden
        res_reg_sources = client.get("/api/v1/admin/resources/sources", headers=headers_reg)
        assert res_reg_sources.status_code == 403

        res_reg_refresh = client.post("/api/v1/admin/resources/refresh", headers=headers_reg)
        assert res_reg_refresh.status_code == 403

        # Admin user access -> 200 OK
        res_admin_sources = client.get("/api/v1/admin/resources/sources", headers=headers_admin)
        assert res_admin_sources.status_code == 200
        assert len(res_admin_sources.json()) >= 5

        res_admin_refresh = client.post("/api/v1/admin/resources/refresh", headers=headers_admin)
        assert res_admin_refresh.status_code == 200
        assert res_admin_refresh.json()["status"] == "success"
    finally:
        db_session.close()

def test_live_fetcher_domain_security_policy():
    from app.services.live_fetcher import fetch_official_live_url, is_official_domain

    assert is_official_domain("https://esankhyiki.mospi.gov.in/macroindicators-main") is True
    assert is_official_domain("https://www.mospi.gov.in/publication") is True
    assert is_official_domain("https://nssta.gov.in/") is True

    # Malicious or unauthorized external domains must be blocked
    assert is_official_domain("https://unverified-thirdparty.com/data") is False
    res = fetch_official_live_url("https://unverified-thirdparty.com/data")
    assert res["success"] is False
    assert "Security Policy Violation" in res["error"]
