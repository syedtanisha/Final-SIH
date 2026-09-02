from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import httpx
from ..models.models import User, Competency, UserCompetency, LearningResource, ResourceCompetencyMapping, QuizAttempt
from ..schemas.competency import (
    UserCompetencyDetail,
    CompetencyProfileOut,
    CompetencyGapItem,
    CompetencyGapAnalysisOut,
    LearningResourceOut,
    RecommendationItem,
    RecommendationResponse,
    LearningPathMilestone,
    LearningPathResponse
)
from ..data.seed_data import DIVISION_PROFILES, DESIGNATION_MODIFIERS
from .ai_service import generate_gap_diagnosis
from ..core.config import settings

def resolve_role_benchmarks(department: str = "", designation: str = "") -> Dict[str, Any]:
    dept_str = (department or "").lower()
    desig_str = (designation or "").lower()

    selected_div_key = None
    for key in DIVISION_PROFILES:
        if "nad" in dept_str or "national accounts" in dept_str:
            if "national accounts" in key.lower():
                selected_div_key = key
                break
        elif "fod" in dept_str or "field operations" in dept_str:
            if "field operations" in key.lower():
                selected_div_key = key
                break
        elif "psd" in dept_str or "price" in dept_str or "economic statistics" in dept_str or "esd" in dept_str:
            if "economic statistics" in key.lower() or "price" in key.lower():
                selected_div_key = key
                break
        elif "sdrd" in dept_str or "survey design" in dept_str:
            if "survey design" in key.lower():
                selected_div_key = key
                break
        elif "dqdd" in dept_str or "data quality" in dept_str or "dissemination" in dept_str:
            if "data quality" in key.lower():
                selected_div_key = key
                break
        elif "des" in dept_str or "state" in dept_str:
            if "state des" in key.lower():
                selected_div_key = key
                break
        elif "niti" in dept_str or "ministry" in dept_str or "line" in dept_str:
            if "ministry line" in key.lower():
                selected_div_key = key
                break

    if not selected_div_key:
        div_profile = {
            "division_code": "GENERAL",
            "description": "General Statistical Professional Cadre",
            "core_competencies": ["STAT_SURVEY", "STAT_COMPUTE", "STAT_NAT_ACC", "STAT_PRICE_IND", "STAT_DATA_GOV"],
            "benchmarks": {
                "STAT_SURVEY": 80.0, "STAT_NAT_ACC": 85.0, "STAT_COMPUTE": 80.0,
                "STAT_PRICE_IND": 75.0, "STAT_LABOUR": 80.0, "STAT_DATA_GOV": 75.0,
                "STAT_QUALITY": 80.0, "STAT_VIZ_COMM": 70.0, "STAT_IND_AGRI": 75.0
            },
            "weights": {
                "STAT_SURVEY": 1.2, "STAT_NAT_ACC": 1.3, "STAT_COMPUTE": 1.2,
                "STAT_PRICE_IND": 1.0, "STAT_LABOUR": 1.1, "STAT_DATA_GOV": 1.0,
                "STAT_QUALITY": 1.1, "STAT_VIZ_COMM": 0.9, "STAT_IND_AGRI": 1.0
            }
        }
    else:
        div_profile = DIVISION_PROFILES[selected_div_key]

    DESIGNATION_ALIASES = {
        "dir": "Director",
        "dg": "Director General",
        "jd": "Joint Director",
        "dd": "Deputy Director",
        "ad": "Assistant Director",
        "sso": "Senior Statistical Officer",
        "jso": "Junior Statistical Officer",
        "si": "Statistical Investigator",
        "fo": "Field Officer"
    }

    desig_clean = desig_str.strip().lower()
    resolution_method = "default"
    delta = 0.0
    weight_mult = 1.0
    seniority = "Statistical Officer"
    role_category = "mid"
    target_difficulty = "Intermediate"

    matched_key = None
    # 1. Exact Normalized Designation Match
    for desig_key in DESIGNATION_MODIFIERS.keys():
        if desig_clean == desig_key.strip().lower():
            matched_key = desig_key
            resolution_method = "exact"
            break

    # 2. Explicit Alias Match
    if not matched_key and desig_clean in DESIGNATION_ALIASES:
        alias_target = DESIGNATION_ALIASES[desig_clean].lower()
        for desig_key in DESIGNATION_MODIFIERS.keys():
            if alias_target in desig_key.lower():
                matched_key = desig_key
                resolution_method = "alias"
                break

    # 3. Substring Keyword Match (longest keyword candidate first)
    if not matched_key:
        sorted_modifiers = sorted(DESIGNATION_MODIFIERS.items(), key=lambda x: len(x[0]), reverse=True)
        for desig_key, modifier in sorted_modifiers:
            if desig_key.lower() in desig_clean:
                matched_key = desig_key
                resolution_method = "keyword"
                break

    if matched_key:
        modifier = DESIGNATION_MODIFIERS[matched_key]
        delta = modifier["benchmark_delta"]
        weight_mult = modifier["weight_multiplier"]
        seniority = modifier["seniority"]
        role_category = modifier.get("role_category", "mid")
        target_difficulty = modifier.get("target_difficulty", "Intermediate")
    else:
        # 4. Ordered Fallback Terms (Whole Word Matching to prevent substring collisions like 'it' in 'title')
        import re
        def match_word(term: str) -> bool:
            return bool(re.search(r'\b' + re.escape(term) + r'\b', desig_clean, re.IGNORECASE))

        if any(match_word(term) for term in ["director", "head", "chief", "advisor", "senior leadership", "secretary", "commissioner"]):
            role_category = "senior"
            target_difficulty = "Advanced"
            seniority = "Senior Leadership"
            delta = 5.0
            weight_mult = 1.12
            resolution_method = "fallback_keyword"
        elif any(match_word(term) for term in ["investigator", "jso", "junior", "field", "enumerator", "collector", "inspector"]):
            role_category = "junior"
            target_difficulty = "Foundational"
            seniority = "Field Operations"
            delta = -1.0
            weight_mult = 0.98
            resolution_method = "fallback_keyword"
        elif any(match_word(term) for term in ["analyst", "scientist", "data", "developer", "engineer", "it", "programmer", "db", "computing"]):
            role_category = "technical"
            target_difficulty = "Advanced"
            seniority = "Technical Data Specialist"
            delta = 2.0
            weight_mult = 1.05
            resolution_method = "fallback_keyword"
        else:
            resolution_method = "default"

    calibrated_benchmarks = {}
    calibrated_weights = {}

    for comp_code, base_val in div_profile["benchmarks"].items():
        # Bounded between 0.0 and 100.0
        calibrated_benchmarks[comp_code] = min(100.0, max(0.0, round(base_val + delta, 1)))

    for comp_code, base_w in div_profile["weights"].items():
        calibrated_weights[comp_code] = max(0.1, round(base_w * weight_mult, 2))

    return {
        "division_name": selected_div_key or "MoSPI Statistical System",
        "division_code": div_profile.get("division_code", "GEN"),
        "cadre_seniority": seniority,
        "role_category": role_category,
        "target_difficulty": target_difficulty,
        "resolution_method": resolution_method,
        "core_competencies": div_profile["core_competencies"],
        "benchmarks": calibrated_benchmarks,
        "weights": calibrated_weights
    }

def calculate_gap(required: float, current: float) -> float:
    return max(0.0, round(required - current, 2))

def get_priority_label(gap: float) -> str:
    if gap >= 30.0:
        return "High"
    elif gap >= 15.0:
        return "Medium"
    elif gap > 0.0:
        return "Low"
    else:
        return "Met"

def get_user_competency_profile(user_id: int, db: Session) -> CompetencyProfileOut:
    user = db.query(User).filter(User.id == user_id).first()
    all_competencies = db.query(Competency).all()
    user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == user_id).all()
    user_comp_map = {uc.competency_id: uc for uc in user_comps}

    role_meta = resolve_role_benchmarks(
        department=user.department if user else "",
        designation=user.designation if user else ""
    )

    details: List[UserCompetencyDetail] = []
    met_count = 0
    gaps_count = 0
    high_priority_gaps = 0
    weighted_achieved_sum = 0.0
    total_weight_sum = 0.0

    for comp in all_competencies:
        uc = user_comp_map.get(comp.id)
        current = uc.current_level if uc else 0.0
        role_req = role_meta["benchmarks"].get(comp.code, comp.required_level)
        role_weight = role_meta["weights"].get(comp.code, 1.0)
        is_core = comp.code in role_meta["core_competencies"]
        
        gap = calculate_gap(role_req, current)
        priority = get_priority_label(gap)

        if gap == 0.0 and current >= role_req:
            met_count += 1
        else:
            gaps_count += 1
            if priority == "High":
                high_priority_gaps += 1

        achievement_ratio = min(1.0, current / role_req) if role_req > 0 else 1.0
        weighted_achieved_sum += (achievement_ratio * role_weight)
        total_weight_sum += role_weight

        details.append(
            UserCompetencyDetail(
                competency_id=comp.id,
                code=comp.code,
                name=comp.name,
                domain=comp.domain,
                description=comp.description,
                required_level=role_req,
                current_level=current,
                gap=gap,
                priority=priority,
                is_role_core=is_core,
                last_assessed_at=uc.last_assessed_at if uc else None
            )
        )

    raw_weighted_score = (weighted_achieved_sum / total_weight_sum * 100.0) if total_weight_sum > 0 else 0.0
    gap_penalty = min(0.15, high_priority_gaps * 0.02)
    overall_readiness = round(max(0.0, raw_weighted_score * (1.0 - gap_penalty)), 1)

    return CompetencyProfileOut(
        overall_readiness_score=overall_readiness,
        total_competencies=len(all_competencies),
        competencies_met_count=met_count,
        active_gaps_count=gaps_count,
        user_division=user.department if user else "MoSPI",
        user_designation=user.designation if user else "Statistical Officer",
        cadre_seniority=role_meta["cadre_seniority"],
        competencies=details
    )

def analyze_competency_gaps(user_id: int, db: Session) -> CompetencyGapAnalysisOut:
    profile = get_user_competency_profile(user_id, db)
    user = db.query(User).filter(User.id == user_id).first()
    
    role_meta = resolve_role_benchmarks(
        department=user.department if user else "",
        designation=user.designation if user else ""
    )

    gap_items: List[CompetencyGapItem] = []
    domain_gap_counts: Dict[str, float] = {}

    for item in profile.competencies:
        role_weight = role_meta["weights"].get(item.code, 1.0)
        priority_score = round(item.gap * role_weight, 2)

        focus_action = f"Complete recommended NSSTA modules & MoSPI study material on {item.name}"
        if item.priority == "High":
            focus_action = f"Immediate priority for {user.department if user else 'your role'}: Study core methodology for {item.name} and take verification quizzes."
        elif item.priority == "Met":
            focus_action = f"Benchmark of {item.required_level}% achieved. Continue periodic refresher assessments."

        gap_items.append(
            CompetencyGapItem(
                competency_id=item.competency_id,
                code=item.code,
                name=item.name,
                domain=item.domain,
                current_level=item.current_level,
                required_level=item.required_level,
                gap=item.gap,
                priority=item.priority,
                priority_score=priority_score,
                is_role_core=item.is_role_core,
                recommended_focus_action=focus_action
            )
        )

        if item.gap > 0:
            domain_gap_counts[item.domain] = domain_gap_counts.get(item.domain, 0.0) + item.gap

    gap_items.sort(key=lambda x: x.priority_score, reverse=True)
    critical_count = sum(1 for g in gap_items if g.priority == "High")

    if domain_gap_counts:
        primary_domain = max(domain_gap_counts.items(), key=lambda x: x[1])[0]
    elif profile.competencies:
        primary_domain = profile.competencies[0].domain
    else:
        primary_domain = "Survey Operations"

    active_gaps = [g.model_dump() if hasattr(g, 'model_dump') else g.dict() for g in gap_items if g.gap > 0]
    ai_summary = generate_gap_diagnosis(
        officer_name=user.full_name if user else "Officer",
        designation=user.designation if user else "Statistical Officer",
        gaps=active_gaps,
        overall_readiness=profile.overall_readiness_score,
        division=user.department if user else "MoSPI"
    )

    return CompetencyGapAnalysisOut(
        total_gaps_identified=len(active_gaps),
        critical_gaps_count=critical_count,
        primary_focus_domain=primary_domain,
        user_division=user.department if user else "MoSPI",
        user_designation=user.designation if user else "Statistical Officer",
        cadre_seniority=role_meta["cadre_seniority"],
        gaps=gap_items,
        ai_diagnosis_summary=ai_summary
    )

def get_personalized_recommendations(user_id: int, db: Session) -> RecommendationResponse:
    user = db.query(User).filter(User.id == user_id).first()
    gap_analysis = analyze_competency_gaps(user_id, db)
    role_meta = resolve_role_benchmarks(user.department if user else "", user.designation if user else "")
    user_role_tier = role_meta.get("role_category", "mid")

    from ..models.models import UserResourceProgress
    completed_res_ids = set()
    if user_id:
        completed_records = db.query(UserResourceProgress).filter(
            UserResourceProgress.user_id == user_id,
            UserResourceProgress.status == "COMPLETED"
        ).all()
        completed_res_ids = {p.resource_id for p in completed_records}

    all_resources = db.query(LearningResource).filter(LearningResource.is_active == True).all()

    if gap_analysis.gaps and gap_analysis.gaps[0].gap > 0:
        top_gap = gap_analysis.gaps[0]
        focus_gap_name = top_gap.name
        focus_gap_code = top_gap.code
        gap_val = top_gap.gap
    else:
        focus_gap_name = "Survey Methodology & Sampling Design"
        focus_gap_code = "STAT_SURVEY"
        gap_val = 0.0

    recommendations: List[RecommendationItem] = []

    for res in all_resources:
        aligned_codes = [m.competency.code for m in res.competency_mappings if m.competency]
        is_direct_match = focus_gap_code in aligned_codes or focus_gap_code in res.title.upper()

        if is_direct_match:
            match_score = 95.0
            reason = f"Directly targets your critical competency gap in {focus_gap_name} ({gap_val}% gap for {user.department if user else 'your division'})."
        elif any(g.code in aligned_codes for g in gap_analysis.gaps[:3]):
            matched_secondary = next((g for g in gap_analysis.gaps[:3] if g.code in aligned_codes), None)
            match_score = 82.0
            reason = f"Targets secondary competency gap in {matched_secondary.name if matched_secondary else 'core statistics'} ({matched_secondary.gap if matched_secondary else 0}% gap)."
        else:
            match_score = 65.0
            reason = f"Core statistical capacity building resource recommended for {user.designation if user else 'officer cadre'}."

        # Official Provenance Preference (+5.0 boost)
        prov_type = res.provenance_type or ""
        if any(term in prov_type for term in ["Official Public Data", "Official Training Resource", "Official Publication", "Official Dataset Catalogue", "Official API"]):
            match_score += 5.0

        # Role Relevance Alignment (+3.0 boost)
        role_rel = res.role_relevance or "all"
        if user_role_tier in role_rel or "all" in role_rel:
            match_score += 3.0

        # Completed Resource Exclusion (excluded from normal recommendations by default)
        if res.id in completed_res_ids:
            continue

        # Access Level Handling
        access_lvl = res.access_level or "PUBLIC"
        if access_lvl in ["REGISTERED", "RESTRICTED"]:
            reason += f" [Access Note: {access_lvl} Access — Registration / Official Credentials Required]."

        first_mapping_prov = res.competency_mappings[0].mapping_provenance if res.competency_mappings and hasattr(res.competency_mappings[0], 'mapping_provenance') else "Platform Curated Competency Mapping"

        res_out = LearningResourceOut(
            id=res.id,
            title=res.title,
            description=res.description,
            source=res.source,
            official_url=res.official_url,
            resource_type=res.resource_type,
            difficulty=res.difficulty,
            estimated_duration_mins=res.estimated_duration_mins,
            publisher_org=res.publisher_org or res.source,
            provenance_type=res.provenance_type,
            reference_period=res.reference_period,
            access_level=access_lvl,
            source_format=res.source_format,
            publication_date=res.publication_date,
            version=res.version,
            thumbnail_url=res.thumbnail_url,
            aligned_competencies=aligned_codes,
            provider_external_id=res.provider_external_id,
            verification_level=res.verification_level or "PORTAL_VERIFIED",
            mapping_provenance=first_mapping_prov
        )

        recommendations.append(
            RecommendationItem(
                resource=res_out,
                matched_competency_code=focus_gap_code,
                matched_competency_name=focus_gap_name,
                competency_gap=gap_val,
                relevance_reason=reason,
                match_score=min(100.0, match_score)
            )
        )

    recommendations.sort(key=lambda x: x.match_score, reverse=True)

    curation_note = (
        f"AI Curated Roadmap for {user.full_name if user else 'Officer'} ({user.department if user else 'MoSPI'}): "
        f"Prioritizing your primary competency gap in {focus_gap_name} ({gap_val}% gap). "
        f"Begin with foundational NSSTA Academy modules to build conceptual mastery, followed by official MoSPI laboratory manuals and eSankhyiki data products. "
        f"Validate each milestone with AI Learning Studio practice quizzes."
    )

    return RecommendationResponse(
        primary_focus_gap=focus_gap_name,
        gap_percentage=gap_val,
        total_recommendations=len(recommendations),
        recommendations=recommendations[:8],
        ai_curation_note=curation_note
    )

def get_personalized_learning_path(user_id: int, db: Session) -> LearningPathResponse:
    user = db.query(User).filter(User.id == user_id).first()
    gap_analysis = analyze_competency_gaps(user_id, db)
    profile = get_user_competency_profile(user_id, db)
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
    user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == user_id).all()

    top_gap = gap_analysis.gaps[0] if gap_analysis.gaps and gap_analysis.gaps[0].gap > 0 else None
    top_gap_name = top_gap.name if top_gap else "Survey Methodology & Sampling Design"
    top_gap_code = top_gap.code if top_gap else "STAT_SURVEY"

    all_resources = db.query(LearningResource).filter(LearningResource.is_active == True).all()
    matched_courses = []
    matched_labs = []
    matched_reports = []

    for r in all_resources:
        aligned = [m.competency.code for m in r.competency_mappings if m.competency]
        if top_gap_code in aligned or any(g.code in aligned for g in gap_analysis.gaps[:2]):
            if r.source == "NSSTA":
                matched_courses.append(r)
            elif r.source == "MoSPI":
                matched_labs.append(r)
            else:
                matched_reports.append(r)

    primary_course = matched_courses[0] if matched_courses else (all_resources[0] if all_resources else None)
    primary_lab = matched_labs[0] if matched_labs else (all_resources[1] if len(all_resources) > 1 else None)

    has_assessed = len(user_comps) > 0 and any(uc.current_level > 0 for uc in user_comps)
    has_gaps_reviewed = has_assessed
    has_taken_quiz = len(attempts) > 0
    has_gained_competency = any(a.competency_delta > 0 for a in attempts)
    interview_ready = profile.overall_readiness_score >= 70.0

    milestones: List[LearningPathMilestone] = [
        LearningPathMilestone(
            phase_number=1,
            title="Step 1: Baseline Diagnostic Assessment",
            domain="Calibration",
            description=f"Complete the calibrated diagnostic test to establish initial benchmark levels across all 9 statistical disciplines tailored for {user.department if user else 'your division'}.",
            recommended_resource="Official Diagnostic Assessment",
            official_url="/assessment",
            estimated_hours=0.5,
            action_type="assessment",
            action_link="/assessment",
            completed=has_assessed,
            competency_code="ALL"
        ),
        LearningPathMilestone(
            phase_number=2,
            title="Step 2: Deterministic Gap Analysis & AI Prescription",
            domain="Diagnostics",
            description=f"Inspect your priority-ranked gaps ($Required - Current = Gap$) and review the AI capacity building prescription for {user.designation if user else 'your cadre'}.",
            recommended_resource="Deterministic Gap Matrix & AI Prescription",
            official_url="/gap-analysis",
            estimated_hours=0.5,
            action_type="assessment",
            action_link="/gap-analysis",
            completed=has_gaps_reviewed,
            competency_code=top_gap_code
        ),
        LearningPathMilestone(
            phase_number=3,
            title=f"Step 3: NSSTA Academy Module — {primary_course.title if primary_course else 'Official Statistical Foundations'}",
            domain="Foundations",
            description=f"Complete the recommended training module at NSSTA to build conceptual mastery in {top_gap_name}.",
            recommended_resource=primary_course.title if primary_course else "NSSTA Official Statistics Module",
            resource_id=primary_course.id if primary_course else None,
            official_url=primary_course.official_url if primary_course else "https://www.mospi.gov.in",
            estimated_hours=3.0,
            action_type="course",
            action_link="/hub?tab=nssta",
            completed=has_taken_quiz,
            competency_code=top_gap_code
        ),
        LearningPathMilestone(
            phase_number=4,
            title=f"Step 4: NSSTA Lab Manual & MoSPI Publication — {primary_lab.title if primary_lab else 'Advanced Statistics Manual'}",
            domain="Applied Skills",
            description=f"Review laboratory manual and MoSPI survey methodology notes for hands-on application in {top_gap_name}.",
            recommended_resource=primary_lab.title if primary_lab else "NSSTA Training Manual",
            resource_id=primary_lab.id if primary_lab else None,
            official_url=primary_lab.official_url if primary_lab else "https://nssta.gov.in",
            estimated_hours=2.5,
            action_type="lab",
            action_link="/hub?tab=nssta",
            completed=has_taken_quiz,
            competency_code=top_gap_code
        ),
        LearningPathMilestone(
            phase_number=5,
            title=f"Step 5: AI Learning Studio Document & Practice Quiz",
            domain="AI Assessment",
            description=f"Generate schema-enforced verification quizzes in the AI Learning Studio from study materials on {top_gap_name}.",
            recommended_resource="AI MCQ Generation & Pedagogical Explanations",
            official_url="/studio",
            estimated_hours=1.0,
            action_type="quiz",
            action_link=f"/studio?topic={top_gap_name}",
            completed=has_taken_quiz,
            competency_code=top_gap_code
        ),
        LearningPathMilestone(
            phase_number=6,
            title="Step 6: Verified Competency Delta Calibration (+Delta Gain)",
            domain="Outcome & Recalibration",
            description="Score >= 75% on generated quizzes to trigger the closed-loop delta update and record demonstrable skill growth (+26%).",
            recommended_resource="Competency Progress Analytics & Growth Delta",
            official_url="/progress",
            estimated_hours=0.5,
            action_type="quiz",
            action_link="/progress",
            completed=has_gained_competency,
            competency_code=top_gap_code
        ),
        LearningPathMilestone(
            phase_number=7,
            title="Step 7: AI Final Interview",
            domain="Capstone Assessment",
            description="Demonstrate comprehensive competency mastery across India's Official Statistical System in an AI-powered conversational interview.",
            recommended_resource="AI Final Interview Readiness & Multi-Domain Evaluation",
            official_url="/final-interview",
            estimated_hours=1.0,
            action_type="interview",
            action_link="/final-interview",
            completed=interview_ready and has_gained_competency,
            competency_code="ALL"
        )
    ]

    completed_count = sum(1 for m in milestones if m.completed)
    progress_pct = int(round((completed_count / len(milestones)) * 100))

    curation_note = (
        f"AI Personalized Learning Roadmap for {user.full_name if user else 'Officer'} ({user.designation if user else 'Cadre'}, {user.department if user else 'MoSPI'}): "
        f"This 7-step progression is synchronized with your role-specific benchmarks. "
        f"Current focus: Bridge the {top_gap.gap if top_gap else 0}% gap in {top_gap_name} to elevate your overall readiness score to {profile.overall_readiness_score}%."
    )

    return LearningPathResponse(
        user_id=user.id if user else 0,
        officer_name=user.full_name if user else "Officer",
        designation=user.designation if user else "Statistical Officer",
        division=user.department if user else "MoSPI",
        overall_readiness_score=profile.overall_readiness_score,
        primary_focus_gap=top_gap_name,
        total_milestones=len(milestones),
        completed_milestones=completed_count,
        progress_percentage=progress_pct,
        milestones=milestones,
        ai_curation_note=curation_note
    )

class IgotKarmayogiClient:
    def __init__(self):
        self.base_url = settings.IGOT_API_BASE_URL
        self.client_id = settings.IGOT_CLIENT_ID
        self.client_secret = settings.IGOT_CLIENT_SECRET
        self.is_sandbox = settings.IGOT_SANDBOX_MODE

    async def get_courses_by_competency(self, competency_code: str) -> List[Dict[str, Any]]:
        if self.is_sandbox or not self.client_id:
            return self._get_sandbox_cbp_catalog(competency_code)
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(
                    f"{self.base_url}/courses/competency/{competency_code}",
                    headers={"X-Client-ID": self.client_id, "X-Client-Secret": self.client_secret}
                )
                if res.status_code == 200:
                    return res.json().get("data", [])
                return self._get_sandbox_cbp_catalog(competency_code)
        except Exception as e:
            print(f"[iGOT Client] Fallback to verified catalog: {e}")
            return self._get_sandbox_cbp_catalog(competency_code)

    def _get_sandbox_cbp_catalog(self, competency_code: str) -> List[Dict[str, Any]]:
        catalog = [
            {
                "course_id": "igot-cbp-101",
                "title": "iGOT: Official Statistics and Survey System in India",
                "provider": "Ministry of Statistics & Programme Implementation",
                "competency_code": "STAT_SURVEY",
                "duration_hours": 3.0,
                "url": "https://igotkarmayogi.gov.in/learn/course/official-statistics-foundations",
                "status": "Available"
            },
            {
                "course_id": "igot-cbp-102",
                "title": "iGOT: Python Programming for Public Policy & Data Analytics",
                "provider": "Digital India Corporation & MoSPI",
                "competency_code": "STAT_COMPUTE",
                "duration_hours": 4.5,
                "url": "https://igotkarmayogi.gov.in/learn/course/python-for-data-analytics",
                "status": "Available"
            },
            {
                "course_id": "igot-cbp-103",
                "title": "iGOT: National Accounts Statistics and SNA 2008 Implementation",
                "provider": "National Statistical Systems Training Academy",
                "competency_code": "STAT_NAT_ACC",
                "duration_hours": 5.0,
                "url": "https://igotkarmayogi.gov.in/learn/course/national-accounts-sna-2008",
                "status": "Available"
            }
        ]
        if competency_code:
            filtered = [c for c in catalog if c["competency_code"] == competency_code]
            return filtered if filtered else catalog
        return catalog

igot_client = IgotKarmayogiClient()

MOSPI_PUBLICATIONS_CATALOG = [
    {
        "title": "National Accounts Statistics (NAS) 2024",
        "category": "Macroeconomic Aggregates",
        "description": "Comprehensive statistical tables on Gross Domestic Product, Gross Capital Formation, and Private Final Consumption Expenditure with 2011-12 base.",
        "url": "https://mospi.gov.in/publication/national-accounts-statistics-2024",
        "aligned_competency": "STAT_NAT_ACC"
    },
    {
        "title": "Periodic Labour Force Survey (PLFS) Annual Report",
        "category": "Socio-Economic Surveys",
        "description": "Estimates of key employment and unemployment indicators in both rural and urban areas for India.",
        "url": "https://mospi.gov.in/publication/periodic-labour-force-survey-annual-report",
        "aligned_competency": "STAT_LABOUR"
    },
    {
        "title": "Annual Survey of Industries (ASI) Summary Results",
        "category": "Industrial Statistics",
        "description": "Factory sector growth, capital invested, output, and net value added in registered manufacturing units.",
        "url": "https://mospi.gov.in/publication/annual-survey-industries",
        "aligned_competency": "STAT_IND_AGRI"
    },
    {
        "title": "eSankhyiki Data Catalogue & Macro Indicators Module",
        "category": "Digital Data Portal",
        "description": "The official one-stop data platform for discovering, filtering, and downloading microdata and time-series indicators.",
        "url": "https://esankhyiki.mospi.gov.in",
        "aligned_competency": "STAT_DATA_GOV"
    },
    {
        "title": "Consumer Price Index (CPI) Technical Manual",
        "category": "Price Statistics",
        "description": "Methodology for collecting rural and urban retail prices, item weighting, and compiling state and all-India CPI (Rural/Urban/Combined).",
        "url": "https://mospi.gov.in/publication/cpi-manual",
        "aligned_competency": "STAT_PRICE_IND"
    }
]

def get_mospi_catalog() -> List[Dict[str, Any]]:
    return MOSPI_PUBLICATIONS_CATALOG

NSSTA_COURSES_CATALOG = [
    {
        "course_code": "NSSTA-TRG-01",
        "title": "Foundational Course in Official Statistics for ISS Officers",
        "duration": "2 Weeks",
        "mode": "In-Person / Blended",
        "description": "Core induction module covering National Accounts, Sample Survey Design, Price Indices, and Data Dissemination.",
        "url": "https://nssta.gov.in/training/iss-foundation",
        "aligned_competency": "STAT_SURVEY"
    },
    {
        "course_code": "NSSTA-TRG-02",
        "title": "Advanced Workshop on Survey Design & Sampling Estimation",
        "duration": "1 Week",
        "mode": "Hands-on Lab",
        "description": "Stratified multi-stage sampling design, variance estimation, and non-sampling error minimization in large-scale NSS surveys.",
        "url": "https://nssta.gov.in/training/survey-design",
        "aligned_competency": "STAT_SURVEY"
    },
    {
        "course_code": "NSSTA-TRG-03",
        "title": "National Accounts Statistics & Input-Output Tables",
        "duration": "1 Week",
        "mode": "Executive Masterclass",
        "description": "Compilation of State Domestic Product (SDP), Gross Value Added (GVA), and SUT (Supply and Use Tables).",
        "url": "https://nssta.gov.in/training/national-accounts",
        "aligned_competency": "STAT_NAT_ACC"
    },
    {
        "course_code": "NSSTA-TRG-04",
        "title": "Data Analytics with R and Python for Official Statisticians",
        "duration": "2 Weeks",
        "mode": "Virtual Lab",
        "description": "Practical data wrangling, web scraping, automated report generation, and data visualization using R and Python.",
        "url": "https://nssta.gov.in/training/python-r-analytics",
        "aligned_competency": "STAT_COMPUTE"
    }
]

def get_nssta_catalog() -> List[Dict[str, Any]]:
    return NSSTA_COURSES_CATALOG
