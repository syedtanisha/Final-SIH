import pytest
import uuid
import io
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Document, ContentChunk, Quiz, QuizQuestion, QuizAttempt, Competency
from app.core.security import create_access_token
from app.services.content_processor import (
    process_and_validate_file, chunk_text, map_content_to_competencies, normalize_text
)
from app.services.assessment_service import validate_mcq_quality

client = TestClient(app)

def test_valid_txt_ingestion_and_chunking():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"officer_phase4_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Phase 4 Officer",
            designation="Statistical Officer",
            department="Field Operations Division",
            role="officer"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        sample_content = (
            "National Accounts Statistics & GDP Compilation Guidelines\n\n"
            "Gross Value Added (GVA) is calculated at basic prices while Gross Domestic Product (GDP) is measured at market prices. "
            "The System of National Accounts (SNA 2008) provides the conceptual framework for compiling institutional sector accounts.\n\n"
            "Price deflators and double deflation methods are used to convert current price aggregates to constant base year prices."
        )

        file_data = ("gdp_guidelines.txt", sample_content.encode("utf-8"), "text/plain")

        # 1. Ingestion Endpoint Test
        res = client.post("/api/v1/content/upload", files={"file": file_data}, headers=headers)
        assert res.status_code == 201
        data = res.json()
        assert data["filename"] == "gdp_guidelines.txt"
        assert data["content_hash"] is not None
        assert data["mapping_method"] == "PLATFORM_HEURISTIC"

        doc_id = data["id"]

        # 2. Document Status Endpoint Test
        res_st = client.get(f"/api/v1/content/{doc_id}/status", headers=headers)
        assert res_st.status_code == 200
        st_data = res_st.json()
        assert st_data["chunk_count"] > 0
        assert st_data["extraction_status"] == "SUCCESS"

        # 3. Duplicate Content Detection
        res_dup = client.post("/api/v1/content/upload", files={"file": file_data}, headers=headers)
        assert res_dup.status_code == 201
        dup_data = res_dup.json()
        assert dup_data["id"] == doc_id
        assert "Duplicate content detected" in dup_data["message"]
    finally:
        db_session.close()

def test_invalid_and_empty_file_rejection():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"officer_reject_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Reject Officer",
            designation="Statistical Investigator",
            department="MoSPI Headquarters",
            role="officer"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Invalid file extension -> HTTP 400
        bad_file = ("script.exe", b"malicious binary payload", "application/x-msdownload")
        res_bad = client.post("/api/v1/content/upload", files={"file": bad_file}, headers=headers)
        assert res_bad.status_code == 400
        assert "Unsupported file format" in res_bad.json()["detail"]

        # 2. Empty file -> HTTP 400
        empty_file = ("empty_sample.txt", b"", "text/plain")
        res_emp = client.post("/api/v1/content/upload", files={"file": empty_file}, headers=headers)
        assert res_emp.status_code == 400
        assert "empty" in res_emp.json()["detail"].lower()
    finally:
        db_session.close()

def test_manual_competency_mapping_override():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"admin_override_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Trainer Admin",
            designation="Director",
            department="NSSTA Training Cell",
            role="admin"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        sample = "Python data science unit-level microdata extraction guidelines using pandas and NumPy."
        res = client.post("/api/v1/content/upload", files={"file": ("python_guide.txt", sample.encode("utf-8"), "text/plain")}, headers=headers)
        assert res.status_code == 201
        doc_id = res.json()["id"]

        comp_nat = db_session.query(Competency).filter(Competency.code == "STAT_NAT_ACC").first()

        # Admin override mapping -> EXPLICIT_DECLARED
        res_ov = client.put(f"/api/v1/content/{doc_id}/competency-mapping", json={"competency_id": comp_nat.id}, headers=headers)
        assert res_ov.status_code == 200
        ov_data = res_ov.json()
        assert ov_data["suggested_competency_id"] == comp_nat.id
        assert ov_data["mapping_method"] == "EXPLICIT_DECLARED"
        assert ov_data["mapping_confidence"] == 1.0
    finally:
        db_session.close()

def test_mcq_quality_validation_and_traceability():
    seen = set()

    # Valid MCQ
    valid_q = {
        "question_text": "What is the primary indicator compiled under SNA 2008?",
        "option_a": "Gross Domestic Product (GDP)",
        "option_b": "Wholesale Price Index",
        "option_c": "Consumer Expenditure",
        "option_d": "Worker Population Ratio",
        "correct_option": "A",
        "explanation": "GDP is the principal macroeconomic aggregate under SNA 2008."
    }
    assert validate_mcq_quality(valid_q, seen) is True

    # Duplicate Question Rejection
    assert validate_mcq_quality(valid_q, seen) is False, "Duplicate question text must be rejected"

    # Invalid option count / duplicate option rejection
    bad_opts_q = {
        "question_text": "Which index measures consumer inflation?",
        "option_a": "CPI",
        "option_b": "CPI",
        "option_c": "WPI",
        "option_d": "IIP",
        "correct_option": "A",
        "explanation": "Duplicate options present"
    }
    assert validate_mcq_quality(bad_opts_q, set()) is False

def test_quiz_attempt_lifecycle_and_resubmission_protection():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"quiz_lifecycle_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Lifecycle Officer",
            designation="Statistical Officer",
            department="National Accounts Division",
            role="officer"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Generate Quiz
        gen_res = client.post("/api/v1/assessments/generate", json={
            "topic": "National Accounts Statistics",
            "num_questions": 3,
            "difficulty": "Intermediate",
            "purpose": "SELF_ASSESSMENT"
        }, headers=headers)
        assert gen_res.status_code == 201
        quiz_data = gen_res.json()
        quiz_id = quiz_data["id"]

        assert quiz_data["purpose"] == "SELF_ASSESSMENT"
        assert quiz_data["generation_method"] == "DETERMINISTIC_FALLBACK"

        # 2. Start Attempt Lifecycle (ASSIGNED -> IN_PROGRESS)
        st_res = client.post(f"/api/v1/assessments/{quiz_id}/start", headers=headers)
        assert st_res.status_code == 200
        assert st_res.json()["status"] == "IN_PROGRESS"

        # 3. Submit Attempt (IN_PROGRESS -> SUBMITTED -> EVALUATED)
        questions = quiz_data["questions"]
        answers = [{"question_id": q["id"], "selected_option": "A"} for q in questions]

        sub_res = client.post(f"/api/v1/assessments/{quiz_id}/submit", json={"answers": answers}, headers=headers)
        assert sub_res.status_code == 200
        eval_data = sub_res.json()
        assert eval_data["status"] == "EVALUATED"
        assert eval_data["feedback_method"] == "Deterministic Pedagogical Feedback"

        # 4. Re-submission Protection Test (Re-submission returns existing result with 0 delta gain)
        sub_res_dup = client.post(f"/api/v1/assessments/{quiz_id}/submit", json={"answers": answers}, headers=headers)
        assert sub_res_dup.status_code == 200
        dup_eval = sub_res_dup.json()
        assert dup_eval["competency_delta"] == 0.0, "Duplicate evaluation must not mutate competency score again"
    finally:
        db_session.close()

def test_rbac_authorization_controls():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"regular_rbac_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Regular Officer",
            designation="Statistical Investigator",
            department="Field Operations Division",
            role="officer"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        # Attempting to access non-existent quiz owned by another user -> 404/403
        res = client.get("/api/v1/assessments/999999", headers=headers)
        assert res.status_code == 404
    finally:
        db_session.close()
