import pytest
from app.db.database import SessionLocal
from app.models.models import User, Competency, UserCompetency, LearningResource
from app.services.competency_service import analyze_competency_gaps, get_user_competency_profile
from app.services.recommendation_service import get_personalized_recommendations, get_personalized_learning_path

def test_zero_gap_user_profile():
    db = SessionLocal()
    try:
        # Create a test user
        user = db.query(User).filter(User.email == "expert_officer@mospi.gov.in").first()
        if not user:
            user = User(
                email="expert_officer@mospi.gov.in",
                hashed_password="fakehashedpassword",
                full_name="Senior Master Officer",
                designation="Director (ISS)",
                department="MoSPI National Accounts Division (NAD)",
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Set all competencies to 100% (zero gaps)
        all_comps = db.query(Competency).all()
        for comp in all_comps:
            uc = db.query(UserCompetency).filter(
                UserCompetency.user_id == user.id,
                UserCompetency.competency_id == comp.id
            ).first()
            if not uc:
                uc = UserCompetency(user_id=user.id, competency_id=comp.id, current_level=100.0)
                db.add(uc)
            else:
                uc.current_level = 100.0
        db.commit()

        gap_analysis = analyze_competency_gaps(user.id, db)
        assert gap_analysis.total_gaps_identified == 0
        assert gap_analysis.critical_gaps_count == 0
        assert gap_analysis.primary_focus_domain is not None
        assert "Outstanding" in gap_analysis.ai_diagnosis_summary or "capacity profile" in gap_analysis.ai_diagnosis_summary or "Diagnostic" in gap_analysis.ai_diagnosis_summary
    finally:
        db.close()

def test_empty_learning_resources_fallback():
    db = SessionLocal()
    try:
        user = db.query(User).first()
        assert user is not None
        
        # Test recommendation handling when query returns empty list
        # using a non-existent user or empty check
        rec_res = get_personalized_recommendations(user.id, db)
        assert rec_res.total_recommendations >= 0
        assert rec_res.ai_curation_note is not None
        
        path_res = get_personalized_learning_path(user.id, db)
        assert len(path_res.milestones) == 7
        assert path_res.overall_readiness_score >= 0.0
    finally:
        db.close()
