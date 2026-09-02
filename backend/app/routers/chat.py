import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db.database import get_db
from ..core.security import get_current_user
from ..models.models import User, ChatSession, ChatMessage
from ..schemas.chat import (
    ChatSessionCreateReq, ChatSessionOut, ChatSessionDetailOut,
    ChatMessageSubmitReq, ChatMessageOut, RetrievedSourceItem
)
from ..services.chat_service import (
    create_chat_session, get_user_chat_sessions, get_chat_session_by_id,
    process_chat_message, delete_chat_session
)

router = APIRouter(prefix="/chat", tags=["AI Conversational Virtual Assistant"])

def _to_message_out(m: ChatMessage) -> ChatMessageOut:
    retrieved_sources = []
    if m.retrieved_chunk_ids:
        try:
            raw_sources = json.loads(m.retrieved_chunk_ids)
            for s in raw_sources:
                retrieved_sources.append(
                    RetrievedSourceItem(
                        document_id=s.get("document_id", 0),
                        chunk_id=s.get("chunk_id", 0),
                        source_reference=s.get("source_reference", ""),
                        snippet=s.get("snippet", "")
                    )
                )
        except Exception:
            pass

    return ChatMessageOut(
        id=m.id,
        session_id=m.session_id,
        role=m.role,
        content=m.content,
        response_method=m.response_method,
        model_provider=m.model_provider,
        retrieval_used=m.retrieval_used or False,
        retrieved_sources=retrieved_sources,
        competency_context_used=m.competency_context_used or False,
        created_at=m.created_at
    )

def _to_session_out(s: ChatSession, db: Session) -> ChatSessionOut:
    msg_count = db.query(ChatMessage).filter(ChatMessage.session_id == s.session_id).count()
    return ChatSessionOut(
        session_id=s.session_id,
        title=s.title,
        status=s.status,
        created_at=s.created_at,
        last_message_at=s.last_message_at,
        message_count=msg_count
    )

@router.post("/sessions", response_model=ChatSessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: ChatSessionCreateReq,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = create_chat_session(current_user.id, payload.title, db)
    return _to_session_out(session, db)

@router.get("/sessions", response_model=List[ChatSessionOut])
def list_my_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = get_user_chat_sessions(current_user.id, db)
    return [_to_session_out(s, db) for s in sessions]

@router.get("/sessions/{session_id}", response_model=ChatSessionDetailOut)
def get_session_details(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = get_chat_session_by_id(session_id, current_user.id, db)
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.session_id).order_by(ChatMessage.created_at.asc()).all()

    return ChatSessionDetailOut(
        session_id=session.session_id,
        title=session.title,
        status=session.status,
        created_at=session.created_at,
        last_message_at=session.last_message_at,
        messages=[_to_message_out(m) for m in messages]
    )

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageOut)
async def send_message_to_session(
    session_id: str,
    payload: ChatMessageSubmitReq,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assistant_msg = await process_chat_message(session_id, current_user.id, payload.message, db)
    return _to_message_out(assistant_msg)

@router.delete("/sessions/{session_id}", status_code=status.HTTP_200_OK)
def delete_session_by_id(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_chat_session(session_id, current_user.id, db)
    return {"message": f"Chat session '{session_id}' deleted successfully."}
