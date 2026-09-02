from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from ..db.database import get_db
from ..core.security import get_current_user
from ..models.models import User, Document, ContentChunk, Competency
from ..schemas.assessment import DocumentUploadResponse, DocumentOut, ContentStatusOut, CompetencyMappingOverrideRequest
from ..services.content_processor import (
    process_and_validate_file, chunk_text, map_content_to_competencies
)

router = APIRouter(tags=["Documents & Content Processing"])

@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File has no filename.")

    file_bytes = await file.read()
    
    # 1. Validation & Extraction via Content Processor Service
    res = process_and_validate_file(file.filename, file_bytes)

    # 2. SHA-256 Duplicate Content Detection
    content_hash = res["content_hash"]
    existing_doc = db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.content_hash == content_hash
    ).first()

    if existing_doc:
        preview = existing_doc.extracted_text[:300] + ("..." if len(existing_doc.extracted_text) > 300 else "")
        return DocumentUploadResponse(
            id=existing_doc.id,
            filename=existing_doc.filename,
            file_type=existing_doc.file_type,
            file_size_bytes=existing_doc.file_size_bytes,
            character_count=existing_doc.character_count,
            preview_text=preview,
            content_hash=existing_doc.content_hash,
            extraction_status=existing_doc.extraction_status,
            processing_status=existing_doc.processing_status,
            suggested_competency_id=existing_doc.suggested_competency_id,
            mapping_method=existing_doc.mapping_method,
            created_at=existing_doc.created_at,
            message="Duplicate content detected. Existing document record retrieved."
        )

    # 3. Create Document Record
    extracted_text = res["extracted_text"]
    mapping_res = map_content_to_competencies(extracted_text, db)

    doc = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_type=res["ext"],
        file_size_bytes=len(file_bytes),
        extracted_text=extracted_text,
        character_count=len(extracted_text),
        content_hash=content_hash,
        extraction_status="SUCCESS",
        processing_status="MAPPED",
        suggested_competency_id=mapping_res["competency_id"],
        mapping_confidence=mapping_res["mapping_confidence"],
        mapping_method=mapping_res["mapping_method"],
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # 4. Chunking
    chunks_data = chunk_text(extracted_text, doc.id)
    for c_item in chunks_data:
        chunk_obj = ContentChunk(
            document_id=doc.id,
            chunk_index=c_item["chunk_index"],
            chunk_text=c_item["chunk_text"],
            character_count=c_item["character_count"],
            token_count_approx=c_item["token_count_approx"],
            created_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        db.add(chunk_obj)

    doc.processing_status = "CHUNKED"
    db.commit()

    preview = extracted_text[:300] + ("..." if len(extracted_text) > 300 else "")

    return DocumentUploadResponse(
        id=doc.id,
        filename=doc.filename,
        file_type=doc.file_type,
        file_size_bytes=doc.file_size_bytes,
        character_count=doc.character_count,
        preview_text=preview,
        content_hash=doc.content_hash,
        extraction_status=doc.extraction_status,
        processing_status=doc.processing_status,
        suggested_competency_id=doc.suggested_competency_id,
        mapping_method=doc.mapping_method,
        created_at=doc.created_at,
        message="Document uploaded, validated, extracted, chunked, and mapped successfully."
    )

@router.get("", response_model=List[DocumentOut])
def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()

@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    return doc

@router.get("/{document_id}/status", response_model=ContentStatusOut)
def get_document_status(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    chunk_count = db.query(ContentChunk).filter(ContentChunk.document_id == doc.id).count()

    return ContentStatusOut(
        document_id=doc.id,
        filename=doc.filename,
        file_type=doc.file_type,
        content_hash=doc.content_hash,
        extraction_status=doc.extraction_status or "SUCCESS",
        processing_status=doc.processing_status or "CHUNKED",
        character_count=doc.character_count,
        chunk_count=chunk_count,
        suggested_competency_id=doc.suggested_competency_id,
        mapping_confidence=doc.mapping_confidence or 0.85,
        mapping_method=doc.mapping_method or "PLATFORM_HEURISTIC"
    )

@router.post("/{document_id}/competency-mapping", response_model=DocumentOut)
@router.put("/{document_id}/competency-mapping", response_model=DocumentOut)
def override_competency_mapping(
    document_id: int,
    payload: CompetencyMappingOverrideRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    comp = db.query(Competency).filter(Competency.id == payload.competency_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competency not found.")

    doc.suggested_competency_id = comp.id
    doc.mapping_confidence = 1.0
    doc.mapping_method = "EXPLICIT_DECLARED"
    doc.mapping_overridden_by = current_user.id
    doc.overridden_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    db.delete(doc)
    db.commit()
    return {"message": f"Document #{document_id} deleted successfully."}
