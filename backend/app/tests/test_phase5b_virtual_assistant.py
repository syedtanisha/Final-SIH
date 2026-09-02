import pytest
import uuid
import io
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Document, ContentChunk, ChatSession, ChatMessage, Competency
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def user_a():
    db = SessionLocal()
    u = User(
        email=f"officer_a_{uuid.uuid4().hex[:6]}@mospi.gov.in",
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
        email=f"officer_b_{uuid.uuid4().hex[:6]}@mospi.gov.in",
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

def test_chat_session_creation_and_listing(user_a):
    user, headers = user_a

    # 1. Create Session
    res = client.post("/api/v1/chat/sessions", json={"title": "National Accounts Query"}, headers=headers)
    assert res.status_code == 201
    s_data = res.json()
    assert s_data["session_id"].startswith("chat-")
    assert s_data["title"] == "National Accounts Query"
    session_id = s_data["session_id"]

    # 2. List Sessions
    res_list = client.get("/api/v1/chat/sessions", headers=headers)
    assert res_list.status_code == 200
    sessions = res_list.json()
    assert any(s["session_id"] == session_id for s in sessions)

def test_cross_user_session_security_isolation(user_a, user_b):
    user1, headers1 = user_a
    user2, headers2 = user_b

    # User A creates a session
    res = client.post("/api/v1/chat/sessions", json={"title": "Private Session A"}, headers=headers1)
    session_id = res.json()["session_id"]

    # User B tries to view User A's session -> 403
    res_b_view = client.get(f"/api/v1/chat/sessions/{session_id}", headers=headers2)
    assert res_b_view.status_code == 403

    # User B tries to send a message to User A's session -> 403
    res_b_msg = client.post(f"/api/v1/chat/sessions/{session_id}/messages", json={"message": "Hack query"}, headers=headers2)
    assert res_b_msg.status_code == 403

    # User B tries to delete User A's session -> 403
    res_b_del = client.delete(f"/api/v1/chat/sessions/{session_id}", headers=headers2)
    assert res_b_del.status_code == 403

def test_empty_and_oversized_message_rejection(user_a):
    user, headers = user_a
    s_res = client.post("/api/v1/chat/sessions", json={"title": "Validation Session"}, headers=headers)
    sess_id = s_res.json()["session_id"]

    # Empty message -> HTTP 400
    res_emp = client.post(f"/api/v1/chat/sessions/{sess_id}/messages", json={"message": "   "}, headers=headers)
    assert res_emp.status_code == 400

    # Oversized message (> 10000 chars) -> HTTP 400 or 422
    big_msg = "A" * 10001
    res_big = client.post(f"/api/v1/chat/sessions/{sess_id}/messages", json={"message": big_msg}, headers=headers)
    assert res_big.status_code in [400, 422]

def test_rag_retrieval_and_source_grounding(user_a):
    user, headers = user_a

    # Upload document for User A
    sample_text = (
        "Gross Value Added (GVA) at basic prices is calculated by subtracting intermediate consumption "
        "from gross output. Taxes on products are added and subsidies are subtracted to arrive at Gross Domestic Product (GDP)."
    )
    doc_res = client.post("/api/v1/content/upload", files={
        "file": ("gva_methodology.txt", sample_text.encode("utf-8"), "text/plain")
    }, headers=headers)
    assert doc_res.status_code == 201

    # Create chat session
    s_res = client.post("/api/v1/chat/sessions", json={"title": "RAG Verification"}, headers=headers)
    sess_id = s_res.json()["session_id"]

    # Query matching uploaded document
    msg_res = client.post(f"/api/v1/chat/sessions/{sess_id}/messages", json={
        "message": "Explain intermediate consumption and GVA calculation"
    }, headers=headers)
    assert msg_res.status_code == 200
    msg_data = msg_res.json()
    print("DEBUG MSG DATA:", msg_data)

    assert msg_data["retrieval_used"] is True
    assert len(msg_data["retrieved_sources"]) > 0
    ref_item = msg_data["retrieved_sources"][0]
    assert "doc:" in ref_item["source_reference"]
    assert "Based on your uploaded learning material" in msg_data["content"]
    assert msg_data["competency_context_used"] is True

def test_no_irrelevant_chunks_retrieved_and_fallback(user_a):
    user, headers = user_a
    s_res = client.post("/api/v1/chat/sessions", json={"title": "Irrelevant Query"}, headers=headers)
    sess_id = s_res.json()["session_id"]

    # Query completely unrelated to any uploaded document
    msg_res = client.post(f"/api/v1/chat/sessions/{sess_id}/messages", json={
        "message": "What is quantum computing entanglement?"
    }, headers=headers)
    assert msg_res.status_code == 200
    msg_data = msg_res.json()

    assert msg_data["retrieval_used"] is False
    assert len(msg_data["retrieved_sources"]) == 0
    assert "No directly relevant uploaded platform document was found" in msg_data["content"]
    assert msg_data["response_method"] == "DETERMINISTIC_FALLBACK"

def test_private_document_isolation_between_users(user_a, user_b):
    user1, headers1 = user_a
    user2, headers2 = user_b

    # User A uploads a private document about secret survey codes
    secret_text = "Secret Survey Code Alpha-999: Confidential multiplier calculation formula for NAD."
    client.post("/api/v1/content/upload", files={
        "file": ("secret_alpha.txt", secret_text.encode("utf-8"), "text/plain")
    }, headers=headers1)

    # User B creates session and asks about secret survey codes
    s_res_b = client.post("/api/v1/chat/sessions", json={"title": "User B Session"}, headers=headers2)
    sess_b_id = s_res_b.json()["session_id"]

    msg_res_b = client.post(f"/api/v1/chat/sessions/{sess_b_id}/messages", json={
        "message": "What is Secret Survey Code Alpha-999 confidential multiplier formula?"
    }, headers=headers2)

    assert msg_res_b.status_code == 200
    data_b = msg_res_b.json()

    # User B MUST NOT retrieve User A's document chunks
    assert data_b["retrieval_used"] is False
    assert len(data_b["retrieved_sources"]) == 0
    assert "Secret Survey Code Alpha-999" not in data_b["content"]

def test_mocked_live_llm_provenance(user_a):
    user, headers = user_a
    s_res = client.post("/api/v1/chat/sessions", json={"title": "LLM Test"}, headers=headers)
    sess_id = s_res.json()["session_id"]

    # Mock call_llm to return a live LLM response string
    with patch("app.services.chat_service.call_llm") as mock_llm:
        mock_llm.return_value = "According to National Accounts principles, Gross Domestic Product (GDP) measures final economic output."
        
        msg_res = client.post(f"/api/v1/chat/sessions/{sess_id}/messages", json={
            "message": "What does GDP measure?"
        }, headers=headers)

        assert msg_res.status_code == 200
        data = msg_res.json()
        assert data["response_method"] == "LIVE_LLM"
        assert "Gross Domestic Product (GDP) measures final economic output" in data["content"]

def test_chat_session_deletion(user_a):
    user, headers = user_a
    s_res = client.post("/api/v1/chat/sessions", json={"title": "To Delete"}, headers=headers)
    sess_id = s_res.json()["session_id"]

    del_res = client.delete(f"/api/v1/chat/sessions/{sess_id}", headers=headers)
    assert del_res.status_code == 200

    # Getting deleted session returns 404
    get_res = client.get(f"/api/v1/chat/sessions/{sess_id}", headers=headers)
    assert get_res.status_code == 404
