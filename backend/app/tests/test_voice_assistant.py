import pytest
import uuid
import base64
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, ChatSession, ChatMessage
from app.services.voice_service import transcribe_audio, synthesize_text_to_speech
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def test_user_and_headers():
    db = SessionLocal()
    email = f"officer_voice_{uuid.uuid4().hex[:6]}@mospi.gov.in"
    user = User(
        email=email,
        hashed_password="hashpassword",
        full_name="Dr. Voice Test Officer",
        designation="Deputy Director (ISS)",
        department="National Accounts Division (NAD)",
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()
    return user, headers


@pytest.mark.anyio
async def test_direct_stt_transcription_service():
    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    res = await transcribe_audio(audio_bytes=dummy_wav, filename="test.wav", language="en")
    assert res.text is not None
    assert len(res.text) > 0
    assert res.confidence > 0.0
    assert res.stt_provider is not None


@pytest.mark.anyio
async def test_direct_tts_synthesis_service():
    res = await synthesize_text_to_speech(text="MoSPI National Accounts Statistics", language="en")
    assert res.audio_base64 is not None
    assert len(res.audio_base64) > 0
    assert res.audio_format in ("mp3", "wav")
    assert res.tts_provider is not None


def test_unauthenticated_voice_endpoints_security():
    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    
    # 1. Transcribe unauthenticated -> 401
    resp1 = client.post("/api/v1/voice/transcribe", files={"file": ("test.wav", dummy_wav, "audio/wav")})
    assert resp1.status_code == 401

    # 2. Synthesize unauthenticated -> 401
    resp2 = client.post("/api/v1/voice/synthesize", json={"text": "Hello"})
    assert resp2.status_code == 401

    # 3. Voice Chat unauthenticated -> 401
    resp3 = client.post("/api/v1/voice/chat", data={"session_id": "session-1"}, files={"file": ("test.wav", dummy_wav, "audio/wav")})
    assert resp3.status_code == 401


def test_authenticated_voice_transcribe_and_synthesize_api(test_user_and_headers):
    user, headers = test_user_and_headers
    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    
    # Transcribe audio endpoint
    res_tr = client.post(
        "/api/v1/voice/transcribe",
        headers=headers,
        files={"file": ("sample_query.wav", dummy_wav, "audio/wav")},
        data={"language": "en"}
    )
    assert res_tr.status_code == 200, res_tr.text
    tr_data = res_tr.json()
    assert "text" in tr_data
    assert "stt_provider" in tr_data

    # Synthesize text endpoint
    res_sy = client.post(
        "/api/v1/voice/synthesize",
        headers=headers,
        json={"text": "National Statistical Systems Training Academy", "language": "en"}
    )
    assert res_sy.status_code == 200, res_sy.text
    sy_data = res_sy.json()
    assert "audio_base64" in sy_data
    assert "tts_provider" in sy_data


def test_authenticated_voice_rag_chat_endpoint(test_user_and_headers):
    user, headers = test_user_and_headers
    
    # Create chat session
    sess_res = client.post("/api/v1/chat/sessions", headers=headers, json={"title": "Voice Assistant Session"})
    assert sess_res.status_code == 201
    session_id = sess_res.json()["session_id"]

    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

    # Submit Voice Chat
    vchat_res = client.post(
        "/api/v1/voice/chat",
        headers=headers,
        data={"session_id": session_id, "language": "en"},
        files={"file": ("spoken_question.wav", dummy_wav, "audio/wav")}
    )
    assert vchat_res.status_code == 200, f"FAILED STATUS: {vchat_res.status_code}, BODY: {vchat_res.text}"
    vc_data = vchat_res.json()
    assert "transcription" in vc_data
    assert "chat_message" in vc_data
    assert vc_data["chat_message"]["role"].lower() == "assistant"
    assert vc_data["audio_base64"] is not None
    assert vc_data["audio_format"] in ("mp3", "wav")
