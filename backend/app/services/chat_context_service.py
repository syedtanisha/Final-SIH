from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.models import User
from .catalog_service import analyze_competency_gaps, get_personalized_recommendations, get_user_competency_profile

def build_officer_chat_context(user_id: int, db: Session) -> Dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}

    profile = get_user_competency_profile(user_id, db)
    gap_analysis = analyze_competency_gaps(user_id, db)
    recs = get_personalized_recommendations(user_id, db)

    top_gaps = []
    for g in gap_analysis.gaps[:3]:
        top_gaps.append({
            "code": g.code,
            "name": g.name,
            "current": g.current_level,
            "target": g.required_level,
            "gap": g.gap,
            "priority": g.priority
        })

    top_rec_title = recs.recommendations[0].resource.title if recs.recommendations else "NSSTA Capacity Building Programme"

    context_summary = (
        f"Officer Cadre: {user.designation} ({user.department}). "
        f"Primary Capacity Building Focus: {gap_analysis.primary_focus_domain} ({profile.overall_readiness_score:.1f}% Overall Readiness). "
        f"Top Priority Gaps: {', '.join([f'{g.name} ({g.gap:.1f}% gap)' for g in gap_analysis.gaps[:2]])}. "
        f"Top Recommended Resource: '{top_rec_title}'."
    )

    return {
        "user_id": user.id,
        "full_name": user.full_name,
        "designation": user.designation,
        "department": user.department,
        "overall_readiness": profile.overall_readiness_score,
        "primary_focus_gap": gap_analysis.primary_focus_domain,
        "top_gaps": top_gaps,
        "top_recommended_resource": top_rec_title,
        "context_summary": context_summary
    }
