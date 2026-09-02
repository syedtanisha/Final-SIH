import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.database import SessionLocal
from app.models.models import User

client = TestClient(app)

def get_auth_headers():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "interview_test@mospi.gov.in").first()
        if not user:
            user = User(
                email="interview_test@mospi.gov.in",
                hashed_password="fakehashpassword",
                full_name="Interview Officer",
                designation="Statistical Officer",
                department="MoSPI"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        token = create_access_token({"sub": str(user.id)})
        return {"Authorization": f"Bearer {token}"}
    finally:
        db.close()



def test_final_interview_missing_fields_validation():
    headers = get_auth_headers()

    # Missing question and answer
    res = client.post("/api/v1/final-interview/evaluate-answer", json={
        "competency": "STAT_SURVEY",
        "domain": "Survey Operations"
    }, headers=headers)
    assert res.status_code == 422

def test_final_interview_invalid_difficulty():
    headers = get_auth_headers()

    res = client.post("/api/v1/final-interview/evaluate-answer", json={
        "question": "Explain sampling weights in NSS surveys.",
        "answer": "Sampling weights are multipliers applied to unit records.",
        "competency": "STAT_SURVEY",
        "domain": "Survey Operations",
        "difficulty": "NonExistentDifficultyLevel"
    }, headers=headers)
    assert res.status_code == 422

def test_final_interview_valid_submission():
    headers = get_auth_headers()

    res = client.post("/api/v1/final-interview/evaluate-answer", json={
        "question": "Explain the role of stratified sampling in reducing survey estimation variance.",
        "answer": "Stratified sampling partitions heterogeneous populations into homogeneous strata, thereby reducing standard error and improving precision for sub-domain estimates.",
        "competency": "STAT_SURVEY",
        "domain": "Survey Operations",
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "score" in data
    assert 0 <= data["score"] <= 10
    assert "evaluation" in data
    assert isinstance(data["strengths"], list)
    assert "next_difficulty" in data
