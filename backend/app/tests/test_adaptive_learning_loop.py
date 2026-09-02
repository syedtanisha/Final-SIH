import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Competency, LearningResource, UserResourceProgress, UserCompetency, LearningProgressHistory
from app.core.security import create_access_token
from app.services.learning_adaptive_service import process_learning_evidence, start_resource_progress, update_resource_progress, complete_resource_progress

client = TestClient(app)

def test_resource_progress_lifecycle():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"officer_adapt_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Adaptive Learning Officer",
            designation="Statistical Officer",
            department="National Accounts Division"
        )
        db_session.add(user)
        db_session.commit()

        resource = db_session.query(LearningResource).first()
        assert resource is not None

        # Start resource
        prog1 = start_resource_progress(db_session, user.id, resource.id)
        assert prog1.status == "IN_PROGRESS"

        # Update progress to 50%
        prog2 = update_resource_progress(db_session, user.id, resource.id, 50.0, time_spent_mins=15)
        assert prog2.progress_percentage == 50.0

        # Complete resource
        comp_res = complete_resource_progress(db_session, user.id, resource.id)
        assert comp_res["status"] == "COMPLETED"

        rec = db_session.query(UserResourceProgress).filter(
            UserResourceProgress.user_id == user.id,
            UserResourceProgress.resource_id == resource.id
        ).first()
        assert rec.status == "COMPLETED"
        assert rec.progress_percentage == 100.0
        assert rec.evidence_processed is True
    finally:
        db_session.close()

def test_evidence_processing_clamping_and_idempotency():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"idemp_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Idempotency Officer",
            designation="Senior Director",
            department="MoSPI Headquarters"
        )
        db_session.add(user)
        comp = db_session.query(Competency).first()
        db_session.commit()

        key = f"test-ev-key-{uuid.uuid4().hex}"

        # First evaluation
        res1 = process_learning_evidence(
            db=db_session,
            user_id=user.id,
            competency_id=comp.id,
            evidence_type="QUIZ_ATTEMPT",
            evidence_key=key,
            score_percentage=100.0,
            difficulty="Advanced"
        )
        assert res1["processed"] is True
        assert res1["delta"] > 0.0

        # Second evaluation with SAME evidence_key -> Idempotency enforced!
        res2 = process_learning_evidence(
            db=db_session,
            user_id=user.id,
            competency_id=comp.id,
            evidence_type="QUIZ_ATTEMPT",
            evidence_key=key,
            score_percentage=100.0,
            difficulty="Advanced"
        )
        assert res2["processed"] is False
        assert res2["delta"] == 0.0

        # Verify score never exceeds 100.0
        for i in range(10):
            process_learning_evidence(
                db=db_session,
                user_id=user.id,
                competency_id=comp.id,
                evidence_type="QUIZ_ATTEMPT",
                evidence_key=f"clamp-key-{i}-{uuid.uuid4().hex}",
                score_percentage=100.0,
                difficulty="Advanced"
            )
        
        final_comp = db_session.query(UserCompetency).filter(
            UserCompetency.user_id == user.id,
            UserCompetency.competency_id == comp.id
        ).first()
        assert final_comp.current_level <= 100.0
    finally:
        db_session.close()

def test_adaptive_learning_path_api():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"api_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="API Adaptive Officer",
            designation="Assistant Director",
            department="Price Statistics Division"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        # GET /api/v1/learning/my-path
        res = client.get("/api/v1/learning/my-path", headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["user_id"] == user.id
        assert "resources_in_progress" in data
        assert "resources_completed" in data
        assert "remaining_gaps" in data

        # GET /api/v1/learning/history
        res_hist = client.get("/api/v1/learning/history", headers=headers)
        assert res_hist.status_code == 200
        assert isinstance(res_hist.json(), list)
    finally:
        db_session.close()

def test_completed_resource_exclusion_from_recommendations():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"excl_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Exclusion Officer",
            designation="Director",
            department="Economic Statistics Division"
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token({"sub": str(user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        # Initial recommendations
        res_init = client.get("/api/v1/recommendations/for-you", headers=headers)
        assert res_init.status_code == 200
        recs = res_init.json()["recommendations"]
        assert len(recs) > 0
        target_res_id = recs[0]["resource"]["id"]

        # Complete the top resource
        complete_resource_progress(db_session, user.id, target_res_id)

        # Subsequent recommendations -> Target resource MUST be excluded!
        res_after = client.get("/api/v1/recommendations/for-you", headers=headers)
        assert res_after.status_code == 200
        recs_after = res_after.json()["recommendations"]
        rec_ids_after = [r["resource"]["id"] for r in recs_after]

        assert target_res_id not in rec_ids_after, f"Completed resource #{target_res_id} should be excluded from recommendations."
    finally:
        db_session.close()

def test_competency_specific_quiz_evidence_isolation():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"iso_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Isolation Officer",
            designation="Deputy Director",
            department="National Accounts Division"
        )
        db_session.add(user)
        competencies = db_session.query(Competency).all()
        assert len(competencies) >= 2
        comp_a = competencies[0]
        comp_b = competencies[1]
        db_session.commit()

        # Update evidence specifically for comp_a
        key_a = f"iso-key-{uuid.uuid4().hex}"
        process_learning_evidence(
            db=db_session,
            user_id=user.id,
            competency_id=comp_a.id,
            evidence_type="QUIZ_ATTEMPT",
            evidence_key=key_a,
            score_percentage=100.0,
            difficulty="Intermediate"
        )

        uc_a = db_session.query(UserCompetency).filter(UserCompetency.user_id == user.id, UserCompetency.competency_id == comp_a.id).first()
        uc_b = db_session.query(UserCompetency).filter(UserCompetency.user_id == user.id, UserCompetency.competency_id == comp_b.id).first()

        assert uc_a is not None and uc_a.current_level > 0.0
        assert uc_b is None, "Unrelated competency B should not receive score gains from Quiz A."
    finally:
        db_session.close()

def test_diminishing_returns_and_realism_bounds():
    db_session = SessionLocal()
    try:
        user = User(
            email=f"dim_officer_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="hash",
            full_name="Diminishing Officer",
            designation="Joint Director",
            department="MoSPI Headquarters"
        )
        db_session.add(user)
        comp = db_session.query(Competency).first()
        db_session.commit()

        # 1. Gain at 0% level
        res_at_0 = process_learning_evidence(
            db=db_session,
            user_id=user.id,
            competency_id=comp.id,
            evidence_type="RESOURCE_COMPLETION",
            evidence_key=f"dim-key-0-{uuid.uuid4().hex}",
            score_percentage=100.0,
            difficulty="Intermediate"
        )
        delta_at_0 = res_at_0["delta"]

        # Set user competency to 80%
        uc = db_session.query(UserCompetency).filter(UserCompetency.user_id == user.id, UserCompetency.competency_id == comp.id).first()
        uc.current_level = 80.0
        db_session.commit()

        # 2. Gain at 80% level (diminishing returns should apply)
        res_at_80 = process_learning_evidence(
            db=db_session,
            user_id=user.id,
            competency_id=comp.id,
            evidence_type="RESOURCE_COMPLETION",
            evidence_key=f"dim-key-80-{uuid.uuid4().hex}",
            score_percentage=100.0,
            difficulty="Intermediate"
        )
        delta_at_80 = res_at_80["delta"]

        assert delta_at_80 < delta_at_0, f"Diminishing returns expected: delta at 80% ({delta_at_80}) should be smaller than delta at 0% ({delta_at_0})."
    finally:
        db_session.close()
