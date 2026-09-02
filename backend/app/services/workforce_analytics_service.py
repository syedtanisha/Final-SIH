from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.models import (
    User, Competency, UserCompetency, BaselineAssignment,
    LearningResource, ResourceCompetencyMapping, UserResourceProgress,
    LearningProgressHistory, QuizAttempt, Document, ChatSession
)
from ..schemas.workforce_analytics import (
    WorkforceOverviewOut, CompetencyAnalyticsOut, CompetencyDistributionItem,
    DepartmentAnalyticsOut, DepartmentBreakdownItem, RoleTierBreakdownItem,
    TrainingEffectivenessOut, CompetencyGainSummaryItem, ProgressionSummaryItem,
    SkillGapIntelligenceOut, CriticalGapSummaryItem, EmergingSkillIntelligenceOut,
    EmergingSkillSignalItem, CapacityForecastOut, EvidenceLevelEnum,
    DataStatusEnum, EmergingSignalEnum
)

def _determine_evidence_level(sample_size: int, record_count: int = 0) -> EvidenceLevelEnum:
    if sample_size == 0:
        return EvidenceLevelEnum.INSUFFICIENT_DATA
    if sample_size >= 10 or record_count >= 15:
        return EvidenceLevelEnum.HIGH_EVIDENCE
    if sample_size >= 3 or record_count >= 5:
        return EvidenceLevelEnum.MODERATE_EVIDENCE
    return EvidenceLevelEnum.LIMITED_EVIDENCE

def _calculate_user_readiness(user_id: int, db: Session) -> float:
    user_comps = db.query(UserCompetency, Competency).join(
        Competency, UserCompetency.competency_id == Competency.id
    ).filter(UserCompetency.user_id == user_id).all()

    if not user_comps:
        return 0.0

    total_req = sum(c.required_level for uc, c in user_comps)
    total_curr = sum(uc.current_level for uc, c in user_comps)
    if total_req == 0:
        return 0.0
    return min(100.0, (total_curr / total_req) * 100.0)

def get_workforce_overview(db: Session) -> WorkforceOverviewOut:
    total_officers = db.query(User).count()

    # Active users: users with resource progress, quiz attempts, or progress history
    active_user_ids = set()
    for row in db.query(UserResourceProgress.user_id).all():
        active_user_ids.add(row[0])
    for row in db.query(QuizAttempt.user_id).all():
        active_user_ids.add(row[0])
    for row in db.query(LearningProgressHistory.user_id).all():
        active_user_ids.add(row[0])
    active_users = len(active_user_ids)

    total_competencies = db.query(Competency).count()

    users = db.query(User).all()
    readiness_scores = []
    meeting_benchmark_count = 0

    for u in users:
        score = _calculate_user_readiness(u.id, db)
        readiness_scores.append(score)
        if score >= 80.0:
            meeting_benchmark_count += 1

    org_readiness = (sum(readiness_scores) / len(readiness_scores)) if readiness_scores else 0.0
    meeting_pct = (meeting_benchmark_count / total_officers * 100.0) if total_officers > 0 else 0.0

    # Count high-priority gaps across all user competencies (gap >= 25.0)
    high_priority_gaps = 0
    all_ucs = db.query(UserCompetency, Competency).join(
        Competency, UserCompetency.competency_id == Competency.id
    ).all()
    for uc, c in all_ucs:
        if (c.required_level - uc.current_level) >= 25.0:
            high_priority_gaps += 1

    evidence_level = _determine_evidence_level(total_officers, len(all_ucs))

    return WorkforceOverviewOut(
        total_officers=total_officers,
        active_users=active_users,
        total_competencies_tracked=total_competencies,
        organization_readiness_score=round(org_readiness, 2),
        high_priority_gap_count=high_priority_gaps,
        officers_meeting_benchmarks_pct=round(meeting_pct, 2),
        evidence_level=evidence_level,
        calculation_method="Deterministic Aggregate Readiness & Benchmark Compliance over UserCompetency DB Records",
        sample_size=total_officers
    )

def get_workforce_competencies(db: Session) -> CompetencyAnalyticsOut:
    total_officers = db.query(User).count()
    competencies = db.query(Competency).all()
    items = []

    for c in competencies:
        ucs = db.query(UserCompetency).filter(UserCompetency.competency_id == c.id).all()
        if ucs:
            avg_current = sum(uc.current_level for uc in ucs) / len(ucs)
            affected_count = sum(1 for uc in ucs if uc.current_level < c.required_level)
            meeting_count = sum(1 for uc in ucs if uc.current_level >= c.required_level)
            meeting_pct = (meeting_count / len(ucs)) * 100.0
        else:
            avg_current = 0.0
            affected_count = total_officers
            meeting_pct = 0.0

        avg_gap = max(0.0, c.required_level - avg_current)
        items.append({
            "code": c.code,
            "name": c.name,
            "domain": c.domain,
            "required_level": c.required_level,
            "average_current_level": round(avg_current, 2),
            "average_gap": round(avg_gap, 2),
            "affected_officers_count": affected_count,
            "meeting_benchmark_pct": round(meeting_pct, 2),
            "raw_gap": avg_gap
        })

    # Sort by raw_gap descending
    items.sort(key=lambda x: x["raw_gap"], reverse=True)

    dist_items = []
    for rank, item in enumerate(items, 1):
        dist_items.append(CompetencyDistributionItem(
            code=item["code"],
            name=item["name"],
            domain=item["domain"],
            required_level=item["required_level"],
            average_current_level=item["average_current_level"],
            average_gap=item["average_gap"],
            affected_officers_count=item["affected_officers_count"],
            meeting_benchmark_pct=item["meeting_benchmark_pct"],
            priority_rank=rank
        ))

    highest_gap_comp = dist_items[0].code if dist_items else "N/A"
    evidence_level = _determine_evidence_level(total_officers, len(dist_items))

    return CompetencyAnalyticsOut(
        competencies=dist_items,
        highest_gap_competency=highest_gap_comp,
        sample_size=total_officers,
        evidence_level=evidence_level,
        calculation_method="Organization-Wide Per-Competency Current Level and Benchmark Gap Aggregation"
    )

def get_workforce_departments(db: Session) -> DepartmentAnalyticsOut:
    users = db.query(User).all()
    total_officers = len(users)

    # Department breakdown
    dept_map: Dict[str, List[User]] = {}
    for u in users:
        dept = u.department or "Unassigned Department"
        dept_map.setdefault(dept, []).append(u)

    dept_items = []
    for dept_name, dept_users in dept_map.items():
        scores = [_calculate_user_readiness(u.id, db) for u in dept_users]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        meeting_count = sum(1 for s in scores if s >= 80.0)
        meeting_pct = (meeting_count / len(dept_users) * 100.0) if dept_users else 0.0

        # Determine primary focus gap in department
        comp_gaps: Dict[str, float] = {}
        for u in dept_users:
            ucs = db.query(UserCompetency, Competency).join(
                Competency, UserCompetency.competency_id == Competency.id
            ).filter(UserCompetency.user_id == u.id).all()
            for uc, c in ucs:
                gap = max(0.0, c.required_level - uc.current_level)
                comp_gaps[c.code] = comp_gaps.get(c.code, 0.0) + gap

        primary_gap = max(comp_gaps.items(), key=lambda x: x[1])[0] if comp_gaps else "STAT_SURVEY"

        dept_items.append(DepartmentBreakdownItem(
            department=dept_name,
            officer_count=len(dept_users),
            average_readiness_score=round(avg_score, 2),
            primary_focus_gap=primary_gap,
            meeting_benchmark_pct=round(meeting_pct, 2)
        ))

    # Role tier breakdown
    assignments = db.query(BaselineAssignment).all()
    tier_user_map: Dict[str, List[int]] = {}
    for a in assignments:
        tier_user_map.setdefault(a.role_tier, []).append(a.user_id)

    # Add unassigned users to "mid" tier as fallback
    assigned_user_ids = {a.user_id for a in assignments}
    for u in users:
        if u.id not in assigned_user_ids:
            tier_user_map.setdefault("mid", []).append(u.id)

    tier_items = []
    for tier_name, u_ids in tier_user_map.items():
        scores = [_calculate_user_readiness(uid, db) for uid in u_ids]
        avg_score = sum(scores) / len(scores) if scores else 0.0

        tier_comp_gaps: Dict[str, float] = {}
        for uid in u_ids:
            ucs = db.query(UserCompetency, Competency).join(
                Competency, UserCompetency.competency_id == Competency.id
            ).filter(UserCompetency.user_id == uid).all()
            for uc, c in ucs:
                gap = max(0.0, c.required_level - uc.current_level)
                tier_comp_gaps[c.code] = tier_comp_gaps.get(c.code, 0.0) + gap

        primary_gap = max(tier_comp_gaps.items(), key=lambda x: x[1])[0] if tier_comp_gaps else "STAT_SURVEY"

        tier_items.append(RoleTierBreakdownItem(
            role_tier=tier_name,
            officer_count=len(u_ids),
            average_readiness_score=round(avg_score, 2),
            primary_focus_gap=primary_gap
        ))

    evidence_level = _determine_evidence_level(total_officers, len(dept_items))

    return DepartmentAnalyticsOut(
        departments=dept_items,
        role_tiers=tier_items,
        sample_size=total_officers,
        evidence_level=evidence_level,
        calculation_method="Department and Role-Tier Grouped Readiness & Primary Gap Resolution"
    )

def get_training_effectiveness(db: Session) -> TrainingEffectivenessOut:
    total_officers = db.query(User).count()
    progress_records = db.query(UserResourceProgress).all()
    attempts = db.query(QuizAttempt).all()
    history = db.query(LearningProgressHistory).all()

    started = sum(1 for p in progress_records if p.status in ["IN_PROGRESS", "COMPLETED"])
    completed = sum(1 for p in progress_records if p.status == "COMPLETED")
    comp_rate = (completed / started * 100.0) if started > 0 else 0.0

    total_attempts = len(attempts)
    avg_quiz_score = (sum(a.score for a in attempts) / total_attempts) if total_attempts > 0 else 0.0
    avg_gain = (sum(h.delta for h in history) / len(history)) if history else 0.0

    # Insufficient data state if no learning activity exists
    if total_attempts == 0 and len(history) == 0 and started == 0:
        return TrainingEffectivenessOut(
            data_status=DataStatusEnum.INSUFFICIENT_DATA,
            resources_started=0,
            resources_completed=0,
            completion_rate_pct=0.0,
            total_quiz_attempts=0,
            average_quiz_score=0.0,
            average_competency_gain=0.0,
            learning_gains_by_competency=[],
            before_after_progression=[],
            sample_size=total_officers,
            evidence_level=EvidenceLevelEnum.INSUFFICIENT_DATA,
            calculation_method="Evidence-Based Learning Activity & Progression Analysis (No Learning Activity Detected)"
        )

    # Gains by competency
    comp_gain_map: Dict[int, List[float]] = {}
    for h in history:
        comp_gain_map.setdefault(h.competency_id, []).append(h.delta)

    gains_by_comp = []
    for comp_id, deltas in comp_gain_map.items():
        c = db.query(Competency).filter(Competency.id == comp_id).first()
        if c:
            gains_by_comp.append(CompetencyGainSummaryItem(
                code=c.code,
                name=c.name,
                total_events=len(deltas),
                avg_gain_delta=round(sum(deltas) / len(deltas), 2),
                max_gain_delta=round(max(deltas), 2)
            ))

    # Before-After progression from attempts or history
    progression = []
    attempt_comp_map: Dict[int, List[QuizAttempt]] = {}
    for a in attempts:
        if a.competency_id:
            attempt_comp_map.setdefault(a.competency_id, []).append(a)

    for comp_id, atts in attempt_comp_map.items():
        c = db.query(Competency).filter(Competency.id == comp_id).first()
        if c:
            avg_before = sum(a.competency_score_before for a in atts) / len(atts)
            avg_after = sum(a.competency_score_after for a in atts) / len(atts)
            avg_delta = sum(a.competency_delta for a in atts) / len(atts)
            progression.append(ProgressionSummaryItem(
                competency_code=c.code,
                avg_before_score=round(avg_before, 2),
                avg_after_score=round(avg_after, 2),
                avg_delta=round(avg_delta, 2)
            ))

    evidence_level = _determine_evidence_level(total_officers, len(history) + total_attempts)

    return TrainingEffectivenessOut(
        data_status=DataStatusEnum.VALID,
        resources_started=started,
        resources_completed=completed,
        completion_rate_pct=round(comp_rate, 2),
        total_quiz_attempts=total_attempts,
        average_quiz_score=round(avg_quiz_score, 2),
        average_competency_gain=round(avg_gain, 2),
        learning_gains_by_competency=gains_by_comp,
        before_after_progression=progression,
        sample_size=total_officers,
        evidence_level=evidence_level,
        calculation_method="Empirical Learning Activity & Quiz Attempt Progression Analysis"
    )

def get_skill_gap_intelligence(db: Session) -> SkillGapIntelligenceOut:
    total_officers = db.query(User).count()
    competencies = db.query(Competency).all()

    top_critical_gaps = []
    for c in competencies:
        ucs = db.query(UserCompetency).filter(UserCompetency.competency_id == c.id).all()
        if ucs:
            avg_current = sum(uc.current_level for uc in ucs) / len(ucs)
            affected_count = sum(1 for uc in ucs if uc.current_level < c.required_level)
        else:
            avg_current = 0.0
            affected_count = total_officers

        avg_gap = max(0.0, c.required_level - avg_current)
        affected_ratio = (affected_count / total_officers) if total_officers > 0 else 0.0

        # Deterministic Priority Formula: (Avg Gap * 0.5) + (Affected Ratio * 30) + (Weight * 20)
        priority_score = (avg_gap * 0.5) + (affected_ratio * 30.0) + ((c.weight or 1.0) * 20.0)

        top_critical_gaps.append(CriticalGapSummaryItem(
            code=c.code,
            name=c.name,
            domain=c.domain,
            avg_gap=round(avg_gap, 2),
            affected_officer_count=affected_count,
            priority_score=round(priority_score, 2),
            formula_explanation="Priority Score = (Avg Gap * 0.5) + (Affected Ratio * 30.0) + (Competency Weight * 20.0)"
        ))

    top_critical_gaps.sort(key=lambda x: x.priority_score, reverse=True)
    highest_priority_code = top_critical_gaps[0].code if top_critical_gaps else "N/A"

    # Department gaps
    depts = db.query(User.department).distinct().all()
    gaps_by_dept: Dict[str, List[str]] = {}
    for d_row in depts:
        dept_name = d_row[0] or "Unassigned Department"
        dept_uids = [u.id for u in db.query(User.id).filter(User.department == dept_name).all()]
        dept_gaps = []
        for c in competencies:
            ucs = db.query(UserCompetency).filter(
                UserCompetency.competency_id == c.id,
                UserCompetency.user_id.in_(dept_uids)
            ).all()
            if ucs:
                avg_curr = sum(uc.current_level for uc in ucs) / len(ucs)
                if (c.required_level - avg_curr) > 15.0:
                    dept_gaps.append(c.code)
            else:
                dept_gaps.append(c.code)
        gaps_by_dept[dept_name] = dept_gaps

    # Role tier gaps
    assignments = db.query(BaselineAssignment).all()
    tier_map: Dict[str, List[int]] = {}
    for a in assignments:
        tier_map.setdefault(a.role_tier, []).append(a.user_id)

    gaps_by_tier: Dict[str, List[str]] = {}
    for tier_name, uids in tier_map.items():
        tier_gaps = []
        for c in competencies:
            ucs = db.query(UserCompetency).filter(
                UserCompetency.competency_id == c.id,
                UserCompetency.user_id.in_(uids)
            ).all()
            if ucs:
                avg_curr = sum(uc.current_level for uc in ucs) / len(ucs)
                if (c.required_level - avg_curr) > 15.0:
                    tier_gaps.append(c.code)
            else:
                tier_gaps.append(c.code)
        gaps_by_tier[tier_name] = tier_gaps

    evidence_level = _determine_evidence_level(total_officers, len(top_critical_gaps))

    return SkillGapIntelligenceOut(
        top_critical_gaps=top_critical_gaps,
        gaps_by_department=gaps_by_dept,
        gaps_by_role_tier=gaps_by_tier,
        highest_training_priority_competency=highest_priority_code,
        priority_formula="Priority Score = (Avg Gap * 0.5) + (Affected Ratio * 30.0) + (Competency Weight * 20.0)",
        sample_size=total_officers,
        evidence_level=evidence_level
    )

def get_emerging_skills(db: Session) -> EmergingSkillIntelligenceOut:
    total_officers = db.query(User).count()
    competencies = db.query(Competency).all()
    signals = []

    for c in competencies:
        ucs = db.query(UserCompetency).filter(UserCompetency.competency_id == c.id).all()
        if ucs:
            affected_count = sum(1 for uc in ucs if uc.current_level < c.required_level)
        else:
            affected_count = total_officers

        affected_pct = (affected_count / total_officers * 100.0) if total_officers > 0 else 0.0
        rec_freq = db.query(ResourceCompetencyMapping).filter(
            ResourceCompetencyMapping.competency_id == c.id
        ).count()
        recent_activity_count = db.query(LearningProgressHistory).filter(
            LearningProgressHistory.competency_id == c.id
        ).count()

        # Rule-based Signal Classification
        if total_officers == 0:
            status = EmergingSignalEnum.INSUFFICIENT_DATA
            rationale = "No officers registered in system to compute emerging skill trends."
        elif affected_pct >= 40.0 and rec_freq >= 2 and total_officers >= 3:
            status = EmergingSignalEnum.EMERGING
            rationale = f"High workforce gap ({affected_pct:.1f}% affected) combined with multi-resource training demand ({rec_freq} mapped resources)."
        elif affected_pct >= 20.0 or recent_activity_count >= 2:
            status = EmergingSignalEnum.GROWING
            rationale = f"Moderate workforce gap ({affected_pct:.1f}%) and active learning progress events ({recent_activity_count} events)."
        else:
            status = EmergingSignalEnum.STABLE
            rationale = f"Low workforce gap ({affected_pct:.1f}%) with stable competency levels across cadres."

        signals.append(EmergingSkillSignalItem(
            competency_code=c.code,
            competency_name=c.name,
            signal_status=status,
            affected_officers_pct=round(affected_pct, 2),
            recommendation_frequency=rec_freq,
            growth_trend=f"{recent_activity_count} verified learning events",
            evidence_rationale=rationale
        ))

    evidence_level = _determine_evidence_level(total_officers, len(signals))

    return EmergingSkillIntelligenceOut(
        signals=signals,
        overall_signal_summary="Rule-based heuristic signal detection evaluating gap ratios, resource mapping frequencies, and historical activity trends.",
        sample_size=total_officers,
        evidence_level=evidence_level,
        calculation_method="Rule-Based Skill Trend Heuristics (Non-ML)"
    )

def get_capacity_forecast(db: Session) -> CapacityForecastOut:
    total_officers = db.query(User).count()
    history = db.query(LearningProgressHistory).all()
    competencies = db.query(Competency).all()

    # Current org readiness
    readiness_scores = [_calculate_user_readiness(u.id, db) for u in db.query(User).all()]
    current_readiness = (sum(readiness_scores) / len(readiness_scores)) if readiness_scores else 0.0

    # Calculate historical gain rate
    if history:
        avg_gain_rate = sum(h.delta for h in history) / len(history)
    else:
        attempts = db.query(QuizAttempt).all()
        if attempts:
            avg_gain_rate = sum(a.competency_delta for a in attempts) / len(attempts)
        else:
            avg_gain_rate = 0.0

    # Check if data is insufficient for forecasting
    if total_officers == 0 or (len(history) == 0 and db.query(QuizAttempt).count() == 0):
        top_priority_codes = [c.code for c in competencies[:3]]
        return CapacityForecastOut(
            forecast_status=DataStatusEnum.INSUFFICIENT_DATA,
            top_priority_training_competencies=top_priority_codes,
            total_officers_needing_capacity_building=total_officers,
            current_organizational_readiness=round(current_readiness, 2),
            projected_readiness_improvement=0.0,
            projected_readiness_60d=round(current_readiness, 2),
            projected_readiness_90d=round(current_readiness, 2),
            historical_gain_rate_per_activity=0.0,
            assumptions=[
                "INSUFFICIENT_DATA: No historical learning progress records or quiz attempts exist.",
                "Readiness projections remain unadjusted at current baseline until verified learning evidence is accumulated.",
                "Assumes 100% linear extrapolation is suppressed when sample size is zero."
            ],
            evidence_level=EvidenceLevelEnum.INSUFFICIENT_DATA,
            calculation_method="Conservative Grounded Readiness Projection (Insufficient Learning History)"
        )

    # Verified historical projections
    projected_imp = min(100.0 - current_readiness, avg_gain_rate * 1.5)
    proj_60d = min(100.0, current_readiness + (avg_gain_rate * 2.0))
    proj_90d = min(100.0, current_readiness + (avg_gain_rate * 3.5))

    # Top priority training competencies (gaps > 20.0)
    top_priority_codes = []
    for c in competencies:
        ucs = db.query(UserCompetency).filter(UserCompetency.competency_id == c.id).all()
        avg_curr = (sum(uc.current_level for uc in ucs) / len(ucs)) if ucs else 0.0
        if (c.required_level - avg_curr) >= 20.0:
            top_priority_codes.append(c.code)
    if not top_priority_codes:
        top_priority_codes = [c.code for c in competencies[:2]]

    officers_needing_cb = sum(1 for s in readiness_scores if s < 80.0)
    evidence_level = _determine_evidence_level(total_officers, len(history))

    assumptions = [
        f"Grounding Assumption: Projections are based strictly on empirical historical learning gain rate ({avg_gain_rate:.2f}% delta per activity).",
        "Linear Progression Limit: Capped at maximum 100.0% organizational readiness.",
        "Participation Assumption: Assumes officers complete planned capacity-building activities over 60–90 days.",
        "No Synthesized Data: No random or unverified ML model parameters were injected."
    ]

    if proj_60d >= 100.0 or proj_90d >= 100.0:
        assumptions.append("DISCLAIMER: Projected 100.0% readiness represents a mathematically capped scenario model, NOT a guaranteed future outcome.")

    return CapacityForecastOut(
        forecast_status=DataStatusEnum.VALID,
        forecast_method="Empirical Historical Gain Rate Extrapolation Model",
        top_priority_training_competencies=top_priority_codes,
        total_officers_needing_capacity_building=officers_needing_cb,
        current_organizational_readiness=round(current_readiness, 2),
        projected_readiness_improvement=round(projected_imp, 2),
        projected_readiness_60d=round(proj_60d, 2),
        projected_readiness_90d=round(proj_90d, 2),
        historical_gain_rate_per_activity=round(avg_gain_rate, 2),
        assumptions=assumptions,
        evidence_level=evidence_level,
        calculation_method="Empirical Historical Gain Rate Extrapolation Model"
    )
