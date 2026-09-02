import pytest
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, BaselineAssignment, LearningResource, OfficialSource, Document, ChatSession, Competency
from app.core.security import create_access_token
from app.services.learning_adaptive_service import process_learning_evidence

client = TestClient(app)

@pytest.fixture
def user_a():
    db = SessionLocal()
    u = User(
        email=f"officer_alpha_{uuid.uuid4().hex[:6]}@mospi.gov.in",
        hashed_password="hash",
        full_name="Officer Alpha",
        designation="Deputy Director",
        department="National Accounts Division",
        role="officer"
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    token = create_access_token({"sub": str(u.id)})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()
    return u, headers

@pytest.fixture
def user_b():
    db = SessionLocal()
    u = User(
        email=f"officer_beta_{uuid.uuid4().hex[:6]}@mospi.gov.in",
        hashed_password="hash",
        full_name="Officer Beta",
        designation="Statistical Investigator",
        department="Field Operations Division",
        role="officer"
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    token = create_access_token({"sub": str(u.id)})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()
    return u, headers

@pytest.fixture
def admin_user():
    db = SessionLocal()
    u = User(
        email=f"admin_hardened_{uuid.uuid4().hex[:6]}@mospi.gov.in",
        hashed_password="hash",
        full_name="System Admin",
        designation="Director General",
        department="MoSPI IT Division",
        role="admin"
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    token = create_access_token({"sub": str(u.id)})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()
    return u, headers

# 1. Security & RBAC Checks
def test_unauthenticated_protected_endpoint_rejection():
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401

def test_non_admin_admin_endpoint_rejection(user_a):
    user, headers = user_a
    res = client.get("/api/v1/admin/analytics/overview", headers=headers)
    assert res.status_code == 403

def test_cross_user_document_isolation(user_a, user_b):
    user1, headers1 = user_a
    user2, headers2 = user_b

    # User A uploads document
    doc_res = client.post("/api/v1/content/upload", files={
        "file": ("doc_a.txt", b"Confidential National Accounts Multipliers Text Data", "text/plain")
    }, headers=headers1)
    doc_id = doc_res.json()["id"]

    # User B tries to view User A's document status -> 403/404
    res_b = client.get(f"/api/v1/content/{doc_id}/status", headers=headers2)
    assert res_b.status_code in [403, 404]

def test_cross_user_chat_isolation(user_a, user_b):
    user1, headers1 = user_a
    user2, headers2 = user_b

    # User A creates chat session
    sess_res = client.post("/api/v1/chat/sessions", json={"title": "Private Chat Session"}, headers=headers1)
    sess_id = sess_res.json()["session_id"]

    # User B tries to view User A's chat session -> 403
    res_b = client.get(f"/api/v1/chat/sessions/{sess_id}", headers=headers2)
    assert res_b.status_code == 403

def test_cross_user_learning_data_isolation(user_a, user_b):
    user1, headers1 = user_a
    user2, headers2 = user_b

    # User A attempts quiz
    q_res = client.post("/api/v1/assessments/generate", json={"topic": "CPI Compilation"}, headers=headers1)
    assert q_res.status_code == 201
    quiz_id = q_res.json()["id"]

    start_res = client.post(f"/api/v1/assessments/{quiz_id}/start", headers=headers1)
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # User B tries to submit User A's quiz attempt -> 403 / 404 / 422
    sub_res = client.post(f"/api/v1/assessments/{quiz_id}/submit", json={
        "attempt_id": attempt_id,
        "answers": {"1": "A"}
    }, headers=headers2)
    assert sub_res.status_code in [403, 404, 422]

def test_client_supplied_identity_spoofing_prevention(user_a, user_b):
    user1, headers1 = user_a
    user2, headers2 = user_b

    # User A calls /auth/me with User B's ID in query parameter -> returns User A's profile
    me_res = client.get(f"/api/v1/auth/me?user_id={user2.id}", headers=headers1)
    assert me_res.status_code == 200
    assert me_res.json()["id"] == user1.id

# 2. Data Integrity Checks
def test_duplicate_baseline_submission_prevention(user_a):
    user, headers = user_a

    # Get baseline questions
    b_res = client.get("/api/v1/assessments/baseline", headers=headers)
    assert b_res.status_code == 200
    b_data = b_res.json()
    assessment_id = b_data["assessment_id"]
    answers = [{"question_id": q["id"], "selected_option": "A"} for q in b_data["questions"]]

    # Submit baseline 1st time -> 200
    sub1 = client.post("/api/v1/assessments/baseline/submit", json={
        "answers": answers
    }, headers=headers)
    assert sub1.status_code == 200

    # Submit baseline 2nd time -> 400 Bad Request
    sub2 = client.post("/api/v1/assessments/baseline/submit", json={
        "answers": answers
    }, headers=headers)
    assert sub2.status_code == 400

def test_duplicate_learning_evidence_idempotency(user_a):
    user, headers = user_a
    db = SessionLocal()
    comp = db.query(Competency).first()
    ev_key = f"test-ev-key-{uuid.uuid4().hex[:6]}"

    # 1st time -> processes delta gain
    res1 = process_learning_evidence(db, user.id, comp.id, "TEST_ACTIVITY", ev_key, 80.0)
    assert res1["delta"] > 0

    # 2nd time -> idempotent 0 delta
    res2 = process_learning_evidence(db, user.id, comp.id, "TEST_ACTIVITY", ev_key, 80.0)
    assert res2["delta"] == 0.0
    db.close()

def test_duplicate_resource_completion_idempotency(user_a):
    user, headers = user_a
    res = client.get("/api/v1/recommendations", headers=headers)
    rec_id = res.json()["recommendations"][0]["resource"]["id"]

    # 1st completion
    c1 = client.post(f"/api/v1/learning/resources/{rec_id}/complete", headers=headers)
    assert c1.status_code == 200
    ev1 = c1.json()["evidence_results"]
    assert len(ev1) > 0

    # 2nd completion -> 0 delta gain (idempotent)
    c2 = client.post(f"/api/v1/learning/resources/{rec_id}/complete", headers=headers)
    assert c2.status_code == 200
    ev2 = c2.json()["evidence_results"]
    assert len(ev2) > 0
    assert ev2[0]["delta"] == 0.0

def test_duplicate_document_upload_handling(user_a):
    user, headers = user_a
    content = f"Unique statistical doc text {uuid.uuid4().hex}"
    
    # 1st upload
    up1 = client.post("/api/v1/content/upload", files={
        "file": ("test_dup.txt", content.encode("utf-8"), "text/plain")
    }, headers=headers)
    assert up1.status_code == 201

    # 2nd upload of identical file content -> Returns existing document
    up2 = client.post("/api/v1/content/upload", files={
        "file": ("test_dup.txt", content.encode("utf-8"), "text/plain")
    }, headers=headers)
    assert up2.status_code in [200, 201]
    assert "already uploaded" in up2.json()["message"].lower() or up2.json()["id"] == up1.json()["id"]

def test_provider_synchronization_idempotency(admin_user):
    admin, headers = admin_user
    res1 = client.post("/api/v1/admin/learning-sources/nssta_tpac/refresh", headers=headers)
    assert res1.status_code == 200
    res2 = client.post("/api/v1/admin/learning-sources/nssta_tpac/refresh", headers=headers)
    assert res2.status_code == 200

# 3. AI Resilience & Provenance Checks
def test_llm_fallback_resilience_and_accurate_provenance(user_a):
    user, headers = user_a
    q_res = client.post("/api/v1/assessments/generate", json={"topic": "Industrial Statistics IIP"}, headers=headers)
    assert q_res.status_code == 201
    q_data = q_res.json()
    assert q_data["generation_method"] == "DETERMINISTIC_FALLBACK"

def test_mcq_quality_validation_post_generation(user_a):
    user, headers = user_a
    q_res = client.post("/api/v1/assessments/generate", json={"topic": "Price Index Numbers"}, headers=headers)
    assert q_res.status_code == 201
    questions = q_res.json()["questions"]
    assert len(questions) > 0
    for q in questions:
        assert q["option_a"] != ""
        assert q["option_b"] != ""
        assert q["option_c"] != ""
        assert q["option_d"] != ""
        assert q["question_text"] != ""

def test_secrets_protection(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/overview", headers=headers)
    res_str = str(res.json())
    assert "SECRET_KEY" not in res_str
    assert "hashed_password" not in res_str

def test_curated_resources_provenance_accuracy(admin_user):
    admin, headers = admin_user
    db = SessionLocal()
    res_list = db.query(LearningResource).filter(LearningResource.source == "iGOT").all()
    for r in res_list:
        assert r.provenance_type in ["Curated Official Metadata", "Official Metadata"]
    db.close()

def test_internal_ids_not_exposed_as_provider_ids(admin_user):
    admin, headers = admin_user
    db = SessionLocal()
    res_list = db.query(LearningResource).all()
    for r in res_list:
        if r.provider_external_id:
            assert r.provider_external_id != str(r.id)
    db.close()

def test_verification_level_transparency(admin_user):
    admin, headers = admin_user
    db = SessionLocal()
    res_list = db.query(LearningResource).all()
    for r in res_list:
        assert r.verification_level in ["PORTAL_VERIFIED", "PAGE_VERIFIED", "RESOURCE_VERIFIED", "UNVERIFIED"]
    db.close()

# 4. Analytics & Forecast Realism Checks
def test_insufficient_data_handling_state(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/training-effectiveness", headers=headers)
    assert res.status_code == 200
    assert res.json()["data_status"] in ["VALID", "INSUFFICIENT_DATA"]

def test_forecast_assumptions_and_disclaimer_transparency(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/capacity-forecast", headers=headers)
    assert res.status_code == 200
    fc = res.json()
    assert "assumptions" in fc
    assert len(fc["assumptions"]) > 0
    assert fc["forecast_method"] != ""

def test_no_fabricated_confidence_metrics(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/overview", headers=headers)
    ov = res.json()
    assert ov["evidence_level"] in ["HIGH_EVIDENCE", "MODERATE_EVIDENCE", "LIMITED_EVIDENCE", "INSUFFICIENT_DATA"]

# 5. Full Regression Check
def test_full_regression_across_all_phases(user_a):
    user, headers = user_a

    # Phase 1: Auth & Profile
    me = client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200

    # Phase 2: Gap Analysis
    gap = client.get("/api/v1/competencies/gap-analysis", headers=headers)
    assert gap.status_code == 200

    # Phase 3: Recommendations
    recs = client.get("/api/v1/recommendations", headers=headers)
    assert recs.status_code == 200

    # Phase 4: Document Upload
    up = client.post("/api/v1/content/upload", files={
        "file": ("regression_doc.txt", b"Regression test document content text.", "text/plain")
    }, headers=headers)
    assert up.status_code in [200, 201]

    # Phase 5B: Chat Assistant
    cs = client.post("/api/v1/chat/sessions", json={"title": "Regression Chat"}, headers=headers)
    assert cs.status_code == 201
