from app.services.progress_service import get_user_progress_summary
from app.db.database import SessionLocal
from app.models.models import User, Competency, UserCompetency, QuizAttempt
from app.main import seed_initial_data

def test_progress_calculation():
    seed_initial_data()
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if user:
            summary = get_user_progress_summary(user.id, db)
            assert summary.user_id == user.id
            assert summary.overall_readiness_score >= 0.0
            assert len(summary.competency_breakdown) > 0
    finally:
        db.close()
