from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional

from ..db.database import get_db
from ..core.security import get_current_user
from ..models.models import User, ChatMessage
from ..schemas.voice import (
    TranscriptionResponse, TTSSynthesisRequest, TTSSynthesisResponse,
    VoiceChatResponse
)
from ..schemas.chat import ChatMessageSubmitReq, ChatMessageOut, RetrievedSourceItem
from ..services.voice_service import (
    transcribe_audio, synthesize_text_to_speech
)
from ..services.chat_service import process_chat_message, get_chat_session_by_id
from ..routers.chat import _to_message_out

router = APIRouter(prefix="/voice", tags=["AI Voice Assistant"])

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_spoken_audio(
    file: UploadFile = File(...),
    language: str = Form("en"),
    current_user: User = Depends(get_current_user)
):
    """
    Upload spoken audio file (.mp3, .wav, .m4a, .webm, .ogg) and receive STT transcription.
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No audio file uploaded."
        )

    try:
        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded audio file is empty (0 bytes)."
            )
        res = await transcribe_audio(audio_bytes=content, filename=file.filename or "audio.wav", language=language)
        return res
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech-to-Text transcription failed: {str(e)}"
        )


@router.post("/synthesize", response_model=TTSSynthesisResponse)
async def synthesize_speech_from_text(
    payload: TTSSynthesisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Synthesize text into spoken audio (mp3 / base64 string).
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text parameter cannot be empty."
        )

    try:
        res = await synthesize_text_to_speech(text=payload.text, language=payload.language or "en")
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text-to-Speech synthesis failed: {str(e)}"
        )


@router.post("/chat", response_model=VoiceChatResponse)
async def voice_rag_chat(
    session_id: str = Form(...),
    language: str = Form("en"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    End-to-End Voice RAG Chat: Upload spoken audio query -> Transcribe -> Process via AI RAG Virtual Assistant -> Synthesize Audio Response.
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No audio file uploaded."
        )

    # 1. Verify Session Ownership
    session = get_chat_session_by_id(session_id, current_user.id, db)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat session '{session_id}' not found."
        )

    # 2. Read & Transcribe Spoken Audio
    try:
        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded audio file is empty (0 bytes)."
            )
        transcription_res = await transcribe_audio(
            audio_bytes=content,
            filename=file.filename or "audio.wav",
            language=language
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audio transcription error: {str(e)}"
        )

    # 3. Process Transcribed Message via Virtual Assistant AI RAG Pipeline
    try:
        assistant_msg = await process_chat_message(
            session_id=session.session_id,
            user_id=current_user.id,
            user_message_text=transcription_res.text,
            db=db
        )
        msg_out = _to_message_out(assistant_msg)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Virtual Assistant AI processing failed: {str(e)}"
        )

    # 4. Synthesize Spoken Audio Response from AI Assistant Answer
    try:
        tts_res = await synthesize_text_to_speech(text=assistant_msg.content, language=language)
        audio_b64 = tts_res.audio_base64
        audio_fmt = tts_res.audio_format
    except Exception as e:
        print(f"[VOICE_ROUTER] Audio synthesis warning: {e}")
        audio_b64 = None
        audio_fmt = "mp3"

    return VoiceChatResponse(
        transcription=transcription_res,
        chat_message=msg_out,
        audio_base64=audio_b64,
        audio_format=audio_fmt
    )
