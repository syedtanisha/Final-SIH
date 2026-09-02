import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import User
from app.core.security import create_access_token

client = TestClient(app)

def create_or_get_user(email: str, name: str, role: str = "user"):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                hashed_password="fakehashedpassword",
                full_name=name,
                designation="Statistical Officer",
                department="MoSPI",
                role=role
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user.id
    finally:
        db.close()

def test_quiz_ownership_isolation():
    user_a_id = create_or_get_user("officer_a@mospi.gov.in", "Officer A")
    user_b_id = create_or_get_user("officer_b@mospi.gov.in", "Officer B")

    token_a = create_access_token({"sub": str(user_a_id)})
    token_b = create_access_token({"sub": str(user_b_id)})

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A generates a quiz
    gen_res = client.post("/api/v1/quizzes/generate", json={
        "topic": "Microdata Anonymization Protocols",
        "custom_text": "Microdata anonymization uses top-coding and k-anonymity to protect statistical respondent identities.",
        "num_questions": 2,
        "difficulty": "Intermediate"
    }, headers=headers_a)
    assert gen_res.status_code == 201
    quiz_id = gen_res.json()["id"]

    # User A can access own quiz
    get_a_res = client.get(f"/api/v1/quizzes/{quiz_id}", headers=headers_a)
    assert get_a_res.status_code == 200

    # User B CANNOT access User A's quiz -> 403 Forbidden
    get_b_res = client.get(f"/api/v1/quizzes/{quiz_id}", headers=headers_b)
    assert get_b_res.status_code == 403
    assert "Access denied" in get_b_res.json()["detail"]

    # User B CANNOT submit answers to User A's quiz -> 403 Forbidden
    submit_b_res = client.post(f"/api/v1/quizzes/{quiz_id}/submit", json={
        "answers": [{"question_id": gen_res.json()["questions"][0]["id"], "selected_option": "A"}]
    }, headers=headers_b)
    assert submit_b_res.status_code == 403
    assert "Access denied" in submit_b_res.json()["detail"]
