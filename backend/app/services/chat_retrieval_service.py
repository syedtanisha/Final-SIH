import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.models import Document, ContentChunk, Competency
from .content_processor import COMPETENCY_KEYWORD_RULES

def detect_query_competency(query: str, db: Session) -> Optional[Competency]:
    query_lower = query.lower()
    matched_code = None

    for code, keywords in COMPETENCY_KEYWORD_RULES.items():
        if any(kw.lower() in query_lower for kw in keywords):
            matched_code = code
            break

    if not matched_code:
        if any(w in query_lower for w in ["survey", "sample", "nsso", "plfs", "stratified"]):
            matched_code = "STAT_SURVEY"
        elif any(w in query_lower for w in ["gdp", "gva", "national accounts", "sna"]):
            matched_code = "STAT_NAT_ACC"
        elif any(w in query_lower for w in ["cpi", "wpi", "iip", "price", "index"]):
            matched_code = "STAT_PRICE_IND"
        elif any(w in query_lower for w in ["python", "r", "pandas", "data science", "compute"]):
            matched_code = "STAT_COMPUTE"

    if matched_code:
        return db.query(Competency).filter(Competency.code == matched_code).first()
    return None

def retrieve_relevant_chunks(
    user_id: int,
    query: str,
    db: Session,
    max_chunks: int = 3
) -> List[Dict[str, Any]]:
    """
    RAG-style retrieval from ContentChunk records.
    Strictly filters Document.user_id == user_id to prevent cross-user document leakage.
    """
    # 1. Get all document IDs belonging ONLY to this user
    user_doc_ids = [
        d.id for d in db.query(Document).filter(Document.user_id == user_id).all()
    ]
    if not user_doc_ids:
        return []

    # 2. Tokenize user query for keyword matching
    query_terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    if not query_terms:
        return []

    # 3. Retrieve chunks belonging to user's documents
    chunks = db.query(ContentChunk).filter(
        ContentChunk.document_id.in_(user_doc_ids)
    ).all()

    scored_chunks = []
    for c in chunks:
        chunk_lower = c.chunk_text.lower()
        score = sum(1 for term in query_terms if term in chunk_lower)
        if score > 0:
            scored_chunks.append((score, c))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    top_chunks = scored_chunks[:max_chunks]
    results = []

    for score, c in top_chunks:
        snippet = c.chunk_text[:200] + ("..." if len(c.chunk_text) > 200 else "")
        results.append({
            "chunk_id": c.id,
            "document_id": c.document_id,
            "source_reference": f"doc:{c.document_id}#chunk:{c.chunk_index}",
            "chunk_text": c.chunk_text,
            "snippet": snippet,
            "relevance_score": score
        })

    return results
