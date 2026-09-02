from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from ..db.database import get_db
from ..core.security import get_current_user
from ..models.models import User, LearningResource
from ..services.sync_service import (
    get_all_provider_statuses, synchronize_provider,
    synchronize_all_providers, PROVIDER_REGISTRY
)

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Learning Sources"])

def enforce_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator authorization required for learning source operations."
        )
    return current_user

@router.get("/learning-sources")
def get_learning_sources(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns list of all configured official learning providers and their current integration statuses.
    """
    return {
        "status": "success",
        "providers": get_all_provider_statuses(db)
    }

@router.post("/learning-sources/{provider_id}/refresh")
def refresh_learning_source(
    provider_id: str,
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Triggers source synchronization and metadata refresh for a specific learning provider.
    """
    if provider_id == "all":
        results = synchronize_all_providers(db)
        return {
            "status": "success",
            "message": "Synchronized all registered official learning providers.",
            "results": results
        }

    try:
        result = synchronize_provider(provider_id, db)
        return {
            "status": "success",
            "message": f"Successfully synchronized provider '{provider_id}'.",
            "result": result
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/learning-sources/{provider_id}/status")
def get_learning_source_status(
    provider_id: str,
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns detailed integration status, mode, provenance breakdown, and resource count for a provider.
    """
    provider = PROVIDER_REGISTRY.get(provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Learning provider '{provider_id}' not found. Available: {list(PROVIDER_REGISTRY.keys())}"
        )

    res_count = db.query(LearningResource).filter(LearningResource.source == provider.name).count()
    resources = db.query(LearningResource).filter(LearningResource.source == provider.name).all()

    provenance_counts: Dict[str, int] = {}
    for r in resources:
        p_type = r.provenance_type or "Curated Official Metadata"
        provenance_counts[p_type] = provenance_counts.get(p_type, 0) + 1

    st = provider.get_status()
    st["resource_count"] = res_count
    st["provenance_breakdown"] = provenance_counts
    return {
        "status": "success",
        "provider": st
    }
