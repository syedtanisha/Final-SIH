from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..core.security import get_current_user
from ..models.models import User
from ..schemas.workforce_analytics import (
    WorkforceOverviewOut, CompetencyAnalyticsOut, DepartmentAnalyticsOut,
    TrainingEffectivenessOut, SkillGapIntelligenceOut, EmergingSkillIntelligenceOut,
    CapacityForecastOut
)
from ..services.workforce_analytics_service import (
    get_workforce_overview, get_workforce_competencies, get_workforce_departments,
    get_training_effectiveness, get_skill_gap_intelligence, get_emerging_skills,
    get_capacity_forecast
)

router = APIRouter(prefix="/api/v1/admin/analytics", tags=["Admin Workforce Analytics"])

def enforce_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin privileges required for workforce analytics."
        )
    return current_user

@router.get("/overview", response_model=WorkforceOverviewOut)
def get_analytics_overview(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns organization-level workforce competency overview, readiness score, and benchmark compliance.
    """
    return get_workforce_overview(db)

@router.get("/competencies", response_model=CompetencyAnalyticsOut)
def get_analytics_competencies(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns organization-wide competency distribution, average scores, gaps, and affected officer counts.
    """
    return get_workforce_competencies(db)

@router.get("/departments", response_model=DepartmentAnalyticsOut)
def get_analytics_departments(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns competency scores, readiness averages, and primary focus gaps grouped by department and role tier.
    """
    return get_workforce_departments(db)

@router.get("/training-effectiveness", response_model=TrainingEffectivenessOut)
def get_analytics_training_effectiveness(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns training completion rates, average quiz scores, and before-versus-after competency progression.
    """
    return get_training_effectiveness(db)

@router.get("/skill-gaps", response_model=SkillGapIntelligenceOut)
def get_analytics_skill_gaps(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns workforce skill-gap aggregation, critical gaps, and department/tier groupings ranked by priority score.
    """
    return get_skill_gap_intelligence(db)

@router.get("/emerging-skills", response_model=EmergingSkillIntelligenceOut)
def get_analytics_emerging_skills(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns rule-based emerging skill signals (EMERGING, GROWING, STABLE, INSUFFICIENT_DATA) and evidence rationale.
    """
    return get_emerging_skills(db)

@router.get("/capacity-forecast", response_model=CapacityForecastOut)
def get_analytics_capacity_forecast(
    current_user: User = Depends(enforce_admin),
    db: Session = Depends(get_db)
):
    """
    Returns conservative workforce capacity building forecast based on verified historical learning gain rates.
    """
    return get_capacity_forecast(db)
