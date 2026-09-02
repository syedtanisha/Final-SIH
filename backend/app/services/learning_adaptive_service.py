import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from ..models.models import (
    User, Competency, UserCompetency, LearningResource,
    UserResourceProgress, LearningProgressHistory, ResourceCompetencyMapping,
    QuizAttempt
)
from .catalog_service import analyze_competency_gaps, get_user_competency_profile, resolve_role_benchmarks

logger = logging.getLogger(__name__)

# Configurable Learning Gain Rules
LEARNING_GAIN_CONFIG = {
    "QUIZ_HIGH_THRESHOLD": 90.0,
    "QUIZ_HIGH_SCORE_GAIN": 15.0,
    "QUIZ_MEDIUM_THRESHOLD": 60.0,
    "QUIZ_MEDIUM_SCORE_GAIN": 10.0,
    "QUIZ_LOW_SCORE_GAIN": 2.0,
    "RESOURCE_COMPLETION_BASE_GAIN": 5.0,
    "DIFFICULTY_MULTIPLIER": {
        "Foundational": 0.8,
        "Intermediate": 1.0,
        "Advanced": 1.3
    },
    "MAX_GAIN_PER_EVENT": 20.0,
    "MAX_COMPETENCY_LEVEL": 100.0,
    "MIN_COMPETENCY_LEVEL": 0.0,
    "DIMINISHING_RETURNS_ENABLED": True
}

def process_learning_evidence(
    db: Session,
    user_id: int,
    competency_id: int,
    evidence_type: str,
    evidence_key: str,
    score_percentage: float = 100.0,
    difficulty: str = "Intermediate",
    relevance_weight: float = 1.0,
    explanation: str = ""
) -> Dict[str, Any]:
    """
    Centralized, deterministic, explainable competency update engine with strict idempotency protection.
    Factors in evidence type, score quality, difficulty, relevance weight, level diminishing returns, and max event cap.
    """
    # 1. Idempotency Guard: Check if evidence_key has already been processed
    if evidence_key:
        existing_history = db.query(LearningProgressHistory).filter(
            LearningProgressHistory.user_id == user_id,
            LearningProgressHistory.evidence_key == evidence_key
        ).first()

        if existing_history:
            logger.info(f"[AdaptiveEngine] Duplicate evidence_key '{evidence_key}' previously processed. Idempotency enforced.")
            return {
                "processed": False,
                "reason": f"Evidence key '{evidence_key}' already processed.",
                "previous_score": existing_history.previous_score,
                "new_score": existing_history.new_score,
                "delta": 0.0,
                "evidence_key": evidence_key
            }

    # 2. Retrieve user competency record
    user_comp = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id,
        UserCompetency.competency_id == competency_id
    ).first()

    if not user_comp:
        user_comp = UserCompetency(
            user_id=user_id,
            competency_id=competency_id,
            current_level=0.0,
            last_assessed_at=datetime.now(timezone.utc).replace(tzinfo=None),
            assessment_source=evidence_type
        )
        db.add(user_comp)
        db.flush()

    prev_score = user_comp.current_level

    # 3. Calculate Deterministic Learning Gain
    diff_mult = LEARNING_GAIN_CONFIG["DIFFICULTY_MULTIPLIER"].get(difficulty, 1.0)
    score_quality = min(1.0, max(0.0, score_percentage / 100.0))

    if evidence_type == "QUIZ_ATTEMPT":
        if score_percentage >= LEARNING_GAIN_CONFIG["QUIZ_HIGH_THRESHOLD"]:
            base = LEARNING_GAIN_CONFIG["QUIZ_HIGH_SCORE_GAIN"]
        elif score_percentage >= LEARNING_GAIN_CONFIG["QUIZ_MEDIUM_THRESHOLD"]:
            base = LEARNING_GAIN_CONFIG["QUIZ_MEDIUM_SCORE_GAIN"]
        else:
            base = LEARNING_GAIN_CONFIG["QUIZ_LOW_SCORE_GAIN"]
        base_gain = base * score_quality
    elif evidence_type == "RESOURCE_COMPLETION":
        base_gain = LEARNING_GAIN_CONFIG["RESOURCE_COMPLETION_BASE_GAIN"]
    else:
        base_gain = score_quality * 15.0

    # Level-based diminishing returns factor (at 0%: 1.0, at 50%: 0.75, at 100%: 0.50)
    level_factor = max(0.2, 1.0 - 0.5 * (prev_score / 100.0))

    raw_gain = base_gain * diff_mult * relevance_weight * level_factor
    capped_gain = min(LEARNING_GAIN_CONFIG["MAX_GAIN_PER_EVENT"], max(0.0, raw_gain))
    new_score = min(LEARNING_GAIN_CONFIG["MAX_COMPETENCY_LEVEL"], max(LEARNING_GAIN_CONFIG["MIN_COMPETENCY_LEVEL"], prev_score + capped_gain))
    delta = round(new_score - prev_score, 2)

    # 4. Update User Competency State
    user_comp.current_level = new_score
    user_comp.last_assessed_at = datetime.now(timezone.utc).replace(tzinfo=None)
    user_comp.assessment_source = evidence_type

    # 5. Persist Auditable History Record
    history_entry = LearningProgressHistory(
        user_id=user_id,
        competency_id=competency_id,
        event_type=evidence_type,
        previous_score=prev_score,
        new_score=new_score,
        delta=delta,
        evidence_key=evidence_key,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(history_entry)
    db.commit()

    logger.info(f"[AdaptiveEngine] User #{user_id} Competency #{competency_id} updated: {prev_score}% -> {new_score}% (+{delta}%) via {evidence_type} [{evidence_key}]")

    return {
        "processed": True,
        "reason": f"Competency updated successfully via {evidence_type}.",
        "previous_score": prev_score,
        "new_score": new_score,
        "delta": delta,
        "evidence_key": evidence_key
    }

def start_resource_progress(db: Session, user_id: int, resource_id: int) -> UserResourceProgress:
    progress = db.query(UserResourceProgress).filter(
        UserResourceProgress.user_id == user_id,
        UserResourceProgress.resource_id == resource_id
    ).first()

    if not progress:
        progress = UserResourceProgress(
            user_id=user_id,
            resource_id=resource_id,
            status="IN_PROGRESS",
            progress_percentage=10.0,
            started_at=datetime.now(timezone.utc).replace(tzinfo=None),
            last_accessed_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        db.add(progress)
    else:
        if progress.status == "NOT_STARTED":
            progress.status = "IN_PROGRESS"
        progress.last_accessed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()
    db.refresh(progress)
    return progress

def update_resource_progress(
    db: Session,
    user_id: int,
    resource_id: int,
    progress_percentage: float,
    time_spent_mins: int = 0
) -> UserResourceProgress:
    progress = start_resource_progress(db, user_id, resource_id)
    progress.progress_percentage = min(100.0, max(0.0, progress_percentage))
    progress.time_spent_mins += time_spent_mins
    progress.last_accessed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    if progress.progress_percentage >= 100.0 and progress.status != "COMPLETED":
        return complete_resource_progress(db, user_id, resource_id)["progress"]

    db.commit()
    db.refresh(progress)
    return progress

def complete_resource_progress(db: Session, user_id: int, resource_id: int) -> Dict[str, Any]:
    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not resource:
        raise ValueError(f"Learning resource ID #{resource_id} not found.")

    progress = db.query(UserResourceProgress).filter(
        UserResourceProgress.user_id == user_id,
        UserResourceProgress.resource_id == resource_id
    ).first()

    if not progress:
        progress = UserResourceProgress(
            user_id=user_id,
            resource_id=resource_id,
            started_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        db.add(progress)

    progress.status = "COMPLETED"
    progress.progress_percentage = 100.0
    progress.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
    progress.last_accessed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    evidence_key = f"res-complete-{user_id}-{resource_id}"
    results = []

    # Process competency evidence for mapped competencies
    mappings = db.query(ResourceCompetencyMapping).filter(ResourceCompetencyMapping.resource_id == resource_id).all()

    for m in mappings:
        res_eval = process_learning_evidence(
            db=db,
            user_id=user_id,
            competency_id=m.competency_id,
            evidence_type="RESOURCE_COMPLETION",
            evidence_key=f"{evidence_key}-comp-{m.competency_id}",
            score_percentage=100.0,
            difficulty=resource.difficulty or "Intermediate",
            relevance_weight=m.relevance_score if hasattr(m, 'relevance_score') and m.relevance_score else 1.0,
            explanation=f"Completed official learning resource: {resource.title}"
        )
        results.append(res_eval)

    progress.evidence_processed = True
    progress.evidence_key = evidence_key
    db.commit()
    db.refresh(progress)

    return {
        "status": "COMPLETED",
        "progress": progress,
        "evidence_results": results
    }

def get_user_learning_progress_history(db: Session, user_id: int) -> List[LearningProgressHistory]:
    return db.query(LearningProgressHistory).filter(LearningProgressHistory.user_id == user_id).order_by(LearningProgressHistory.created_at.desc()).all()
