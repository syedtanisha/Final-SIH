import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.models import ChatSession, ChatMessage, User
from .chat_retrieval_service import retrieve_relevant_chunks, detect_query_competency
from .chat_context_service import build_officer_chat_context
from .ai_service import call_llm
from ..core.config import settings

def create_chat_session(user_id: int, title: Optional[str], db: Session) -> ChatSession:
    sess_id = f"chat-{uuid.uuid4().hex[:12]}"
    session_title = (title or "Capacity Building Assistant Session").strip()
    if not session_title:
        session_title = "Capacity Building Assistant Session"

    session = ChatSession(
        session_id=sess_id,
        user_id=user_id,
        title=session_title,
        status="active",
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        last_message_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_user_chat_sessions(user_id: int, db: Session) -> List[ChatSession]:
    return db.query(ChatSession).filter(
        ChatSession.user_id == user_id,
        ChatSession.status == "active"
    ).order_by(ChatSession.last_message_at.desc()).all()

def get_chat_session_by_id(session_id: str, user_id: int, db: Session) -> ChatSession:
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.status == "active"
    ).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found.")
    if session.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: You do not own this chat session.")
    return session

def delete_chat_session(session_id: str, user_id: int, db: Session) -> bool:
    session = get_chat_session_by_id(session_id, user_id, db)
    session.status = "deleted"
    db.commit()
    return True

async def process_chat_message(
    session_id: str,
    user_id: int,
    user_message_text: str,
    db: Session
) -> ChatMessage:
    if not user_message_text or not user_message_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message content cannot be empty.")
    if len(user_message_text) > 10000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message size exceeds maximum limit of 10,000 characters.")

    session = get_chat_session_by_id(session_id, user_id, db)
    clean_msg = user_message_text.strip()

    # 1. Save User Message
    user_msg_rec = ChatMessage(
        session_id=session.session_id,
        user_id=user_id,
        role="USER",
        content=clean_msg,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(user_msg_rec)
    db.commit()

    # 2. Competency Detection & RAG Retrieval
    detected_comp = detect_query_competency(clean_msg, db)
    retrieved_chunks = retrieve_relevant_chunks(user_id, clean_msg, db, max_chunks=3)
    retrieval_used = len(retrieved_chunks) > 0

    # 3. Officer Context
    officer_ctx = build_officer_chat_context(user_id, db)
    comp_ctx_used = bool(officer_ctx)

    # 4. Bounded Conversation History (recent 6 messages)
    history_msgs = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.session_id
    ).order_by(ChatMessage.created_at.desc()).limit(6).all()
    history_msgs.reverse()

    # 5. Build LLM Prompt
    system_prompt = (
        "You are the AI Statistical Capacity Building Virtual Assistant for India's Official Statistical System (MoSPI / NSSTA).\n"
        "Your task is to assist statistical officers with official statistical concepts, national accounts (SNA 2008), survey sampling designs (PLFS, NSSO), price indices (CPI, WPI, IIP), data analytics, and their personal learning gaps.\n\n"
        f"OFFICER CONTEXT: {officer_ctx.get('context_summary', 'MoSPI Officer Cadre')}\n"
    )

    if retrieval_used:
        doc_refs_str = "\n---\n".join([
            f"[Source: {c['source_reference']}]\n{c['chunk_text']}" for c in retrieved_chunks
        ])
        retrieved_prompt_section = f"\nRETRIEVED UPLOADED MATERIAL:\n{doc_refs_str}\n---\n"
    else:
        retrieved_prompt_section = "\nRETRIEVED UPLOADED MATERIAL: None found for this question.\n"

    history_str = "\n".join([f"{m.role}: {m.content}" for m in history_msgs[:-1]])
    user_prompt = f"{retrieved_prompt_section}\nRECENT CONVERSATION:\n{history_str}\n\nUSER QUESTION: {clean_msg}"

    # 6. Call Multi-Provider LLM
    raw_llm_response = await call_llm(user_prompt, system_prompt=system_prompt)

    response_method = "DETERMINISTIC_FALLBACK"
    model_provider = None

    if raw_llm_response and len(raw_llm_response.strip()) > 10:
        response_method = "LIVE_LLM"
        if settings.GROK_API_KEY or settings.XAI_API_KEY:
            model_provider = "xAI Grok"
        elif settings.GROQ_API_KEY:
            model_provider = "Groq Llama-3.3"
        elif settings.GEMINI_API_KEY:
            model_provider = "Google Gemini"
        else:
            model_provider = "Configured AI Provider"
        final_answer = raw_llm_response.strip()
    else:
        # Structured Deterministic Fallback Response
        response_method = "DETERMINISTIC_FALLBACK"
        model_provider = "MoSPI Deterministic Guidance Engine"

        sources_ref_str = ", ".join([c["source_reference"] for c in retrieved_chunks])

        if retrieval_used:
            lead_in = f"Based on your uploaded learning material ({sources_ref_str}):\n\n"
            extracted_snippet = retrieved_chunks[0]["chunk_text"]
            body_text = f"{extracted_snippet}\n\n"
        else:
            lead_in = "No directly relevant uploaded platform document was found for this query.\n\n"
            body_text = ""

        if detected_comp:
            comp_guidance = (
                f"Regarding {detected_comp.name} ({detected_comp.code}):\n"
                f"This relates to your capacity building profile in {officer_ctx.get('department', 'MoSPI')}. "
                f"I recommend studying the official NSSTA training guidelines and eSankhyiki data products aligned with {detected_comp.code}. "
                f"Your current focus gap: {officer_ctx.get('primary_focus_gap', 'Core Statistics')}."
            )
        else:
            comp_guidance = (
                f"As a {officer_ctx.get('designation', 'Statistical Officer')}, maintaining conceptual rigor across MoSPI methodologies is essential. "
                f"I recommend reviewing your top recommended learning resource: '{officer_ctx.get('top_recommended_resource', 'NSSTA Modules')}'."
            )

        final_answer = f"{lead_in}{body_text}{comp_guidance}"

    # 7. Format Retrieved Sources Metadata JSON
    retrieved_sources_metadata = [
        {
            "document_id": c["document_id"],
            "chunk_id": c["chunk_id"],
            "source_reference": c["source_reference"],
            "snippet": c["snippet"]
        }
        for c in retrieved_chunks
    ]

    assistant_msg_rec = ChatMessage(
        session_id=session.session_id,
        user_id=user_id,
        role="ASSISTANT",
        content=final_answer,
        response_method=response_method,
        model_provider=model_provider,
        retrieval_used=retrieval_used,
        retrieved_chunk_ids=json.dumps(retrieved_sources_metadata) if retrieved_sources_metadata else None,
        competency_context_used=comp_ctx_used,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(assistant_msg_rec)

    session.last_message_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(assistant_msg_rec)

    return assistant_msg_rec
