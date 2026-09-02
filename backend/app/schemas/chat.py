from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatSessionCreateReq(BaseModel):
    title: Optional[str] = Field("Capacity Building Assistant Session", max_length=255)

class RetrievedSourceItem(BaseModel):
    document_id: int
    chunk_id: int
    source_reference: str
    snippet: Optional[str] = None

class ChatMessageOut(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    response_method: Optional[str] = None
    model_provider: Optional[str] = None
    retrieval_used: bool = False
    retrieved_sources: List[RetrievedSourceItem] = []
    competency_context_used: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionOut(BaseModel):
    session_id: str
    title: str
    status: str
    created_at: datetime
    last_message_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True

class ChatSessionDetailOut(BaseModel):
    session_id: str
    title: str
    status: str
    created_at: datetime
    last_message_at: datetime
    messages: List[ChatMessageOut]

    class Config:
        from_attributes = True

class ChatMessageSubmitReq(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="User question or query for the AI virtual assistant.")
