import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.database import SessionLocal
from app.models.models import User
from app.services.ai_service import generate_mcqs_from_text

client = TestClient(app)

def get_auth_headers():
    db = SessionLocal()
    try:
        user = db.query(User).first()
        token = create_access_token({"sub": str(user.id)})
        return {"Authorization": f"Bearer {token}"}
    finally:
        db.close()

def test_mcq_generation_schema():
    text = "The Periodic Labour Force Survey (PLFS) collects data on employment and unemployment using UPSS and CWS."
    questions = generate_mcqs_from_text(text=text, topic="PLFS Labour Methodology", num_questions=3, difficulty="Intermediate")
    
    assert len(questions) == 3
    for q in questions:
        assert "question_text" in q
        assert "option_a" in q
        assert "option_b" in q
        assert "option_c" in q
        assert "option_d" in q
        assert q["correct_option"] in ["A", "B", "C", "D"]
        assert len(q["explanation"]) > 10

def test_quiz_generate_normal_valid_request():
    headers = get_auth_headers()
    res = client.post("/api/v1/quizzes/generate", json={
        "topic": "National Accounts GVA",
        "custom_text": "Gross Value Added at basic prices equals output minus intermediate consumption.",
        "num_questions": 3,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert len(data["questions"]) == 3

def test_quiz_generate_boundary_num_questions():
    headers = get_auth_headers()
    
    # Boundary: min = 1
    res_min = client.post("/api/v1/quizzes/generate", json={
        "topic": "Sampling Theory",
        "num_questions": 1,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res_min.status_code == 201
    
    # Boundary: max = 20
    res_max = client.post("/api/v1/quizzes/generate", json={
        "topic": "Sampling Theory",
        "num_questions": 20,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res_max.status_code == 201

def test_quiz_generate_num_questions_out_of_range():
    headers = get_auth_headers()
    
    # num_questions = 0 -> rejected
    res_zero = client.post("/api/v1/quizzes/generate", json={
        "topic": "Sampling Theory",
        "num_questions": 0,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res_zero.status_code == 422
    
    # num_questions = 21 -> rejected
    res_high = client.post("/api/v1/quizzes/generate", json={
        "topic": "Sampling Theory",
        "num_questions": 21,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res_high.status_code == 422

def test_quiz_generate_topic_exceeding_max_length():
    headers = get_auth_headers()
    
    # topic > 500 chars -> rejected
    long_topic = "A" * 501
    res = client.post("/api/v1/quizzes/generate", json={
        "topic": long_topic,
        "num_questions": 3,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res.status_code == 422

def test_quiz_generate_custom_text_exceeding_max_length():
    headers = get_auth_headers()
    
    # custom_text > 50000 chars -> rejected
    long_text = "A" * 50001
    res = client.post("/api/v1/quizzes/generate", json={
        "topic": "Valid Topic",
        "custom_text": long_text,
        "num_questions": 3,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res.status_code == 422
