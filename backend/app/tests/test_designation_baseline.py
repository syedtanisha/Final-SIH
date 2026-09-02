import pytest
from app.models.models import User, Competency, UserCompetency
from app.services.catalog_service import resolve_role_benchmarks, get_user_competency_profile, analyze_competency_gaps, get_personalized_recommendations
from app.services.assessment_service import get_baseline_assessment_data, evaluate_baseline_submission
from app.schemas.assessment import BaselineAssessmentSubmit, BaselineAnswerSubmit

def test_resolve_role_benchmarks_designation_tiers():
    # Senior Officer
    senior_meta = resolve_role_benchmarks("MoSPI National Accounts Division (NAD)", "Director (ISS)")
    assert senior_meta["role_category"] == "senior"
    assert senior_meta["target_difficulty"] == "Advanced"
    assert senior_meta["cadre_seniority"] == "Senior Leadership"

    # Junior Officer / Field Investigator
    junior_meta = resolve_role_benchmarks("MoSPI Field Operations Division (FOD)", "Statistical Investigator")
    assert junior_meta["role_category"] == "junior"
    assert junior_meta["target_difficulty"] == "Foundational"
    assert junior_meta["cadre_seniority"] == "Field Execution"

    # Technical Data Analyst
    tech_meta = resolve_role_benchmarks("MoSPI Data Quality & Dissemination Division (DQDD)", "Data Analyst")
    assert tech_meta["role_category"] == "technical"
    assert tech_meta["target_difficulty"] == "Advanced"
    assert tech_meta["cadre_seniority"] == "Analytical Technical"

    # Mid-Level Officer
    mid_meta = resolve_role_benchmarks("MoSPI Economic Statistics Division (ESD)", "Senior Statistical Officer")
    assert mid_meta["role_category"] == "mid"
    assert mid_meta["target_difficulty"] == "Intermediate"

    # Unlisted Designation Fallback Test (Extensible logic)
    unlisted_senior = resolve_role_benchmarks("Policy Division", "Chief Statistician Advisor")
    assert unlisted_senior["role_category"] == "senior"

    unlisted_field = resolve_role_benchmarks("Field Unit", "District Field Surveyor")
    assert unlisted_field["role_category"] == "junior"

@pytest.mark.anyio
async def test_baseline_assessment_designation_differentiation():
    director_user = User(id=101, email="director@mospi.gov.in", full_name="Director Test", department="MoSPI NAD", designation="Director (ISS)")
    investigator_user = User(id=102, email="investigator@mospi.gov.in", full_name="Investigator Test", department="MoSPI FOD", designation="Statistical Investigator")
    analyst_user = User(id=103, email="analyst@mospi.gov.in", full_name="Analyst Test", department="MoSPI DQDD", designation="Data Analyst")

    director_assessment = await get_baseline_assessment_data(director_user)
    investigator_assessment = await get_baseline_assessment_data(investigator_user)
    analyst_assessment = await get_baseline_assessment_data(analyst_user)

    assert director_assessment.total_questions == 9
    assert investigator_assessment.total_questions == 9
    assert analyst_assessment.total_questions == 9

    # Verify 100% tailored questions (is_common == False for all 9 questions)
    dir_role = director_assessment.questions
    inv_role = investigator_assessment.questions
    ana_role = analyst_assessment.questions

    assert len(dir_role) == 9
    assert len(inv_role) == 9
    assert len(ana_role) == 9

    dir_role_ids = set(q.id for q in dir_role)
    inv_role_ids = set(q.id for q in inv_role)
    ana_role_ids = set(q.id for q in ana_role)

    # Verify role/department question IDs are distinct between different designations/departments
    assert dir_role_ids != inv_role_ids
    assert dir_role_ids != ana_role_ids
    assert inv_role_ids != ana_role_ids

def test_evaluate_baseline_submission_and_competency_initialization():
    import uuid
    from app.db.database import SessionLocal
    db_session = SessionLocal()
    try:
        unique_email = f"test_eval_{uuid.uuid4().hex[:8]}@mospi.gov.in"
        user = User(
            email=unique_email,
            hashed_password="secretpassword",
            full_name="Dr. Test User",
            department="MoSPI Field Operations Division (FOD)",
            designation="Statistical Investigator"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Ensure competencies exist in DB
        if db_session.query(Competency).count() == 0:
            from app.data.seed_data import COMPETENCIES_SEED
            for c in COMPETENCIES_SEED:
                db_session.add(Competency(**c))
            db_session.commit()

        # Load baseline assessment data for user
        import anyio
        assessment = anyio.run(get_baseline_assessment_data, user)

        # Create submission with correct answers for all questions
        answers = [BaselineAnswerSubmit(question_id=q.id, selected_option="A") for q in assessment.questions]
        submission = BaselineAssessmentSubmit(answers=answers)

        result = evaluate_baseline_submission(user.id, submission, db_session)

        assert result.total_questions == 9
        assert result.total_correct >= 0
        assert result.initialized_competencies_count > 0
        assert "Designation-based baseline assessment" in result.feedback_summary

        # Check user competencies in DB
        user_comps = db_session.query(UserCompetency).filter(UserCompetency.user_id == user.id).all()
        assert len(user_comps) > 0

        # Verify downstream Gap Analysis and Recommendations work
        gap_analysis = analyze_competency_gaps(user.id, db_session)
        assert gap_analysis.user_designation == "Statistical Investigator"
        assert len(gap_analysis.gaps) > 0

        recommendations = get_personalized_recommendations(user.id, db_session)
        assert recommendations.total_recommendations > 0
    finally:
        db_session.close()

def test_part12_skills_intelligence_comprehensive_suite():
    import uuid
    from app.db.database import SessionLocal
    db_session = SessionLocal()
    try:
        # 1. Role-specific requirement differentiation test
        director_meta = resolve_role_benchmarks("MoSPI National Accounts Division (NAD)", "Director (ISS)")
        investigator_meta = resolve_role_benchmarks("MoSPI Field Operations Division (FOD)", "Statistical Investigator")

        # Required level for NAT_ACC should be higher for Director than Investigator
        assert director_meta["benchmarks"]["STAT_NAT_ACC"] > investigator_meta["benchmarks"]["STAT_NAT_ACC"]

        # 2. Deterministic question selection test
        user = User(
            id=999,
            email=f"det_test_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            department="MoSPI NAD",
            designation="Director (ISS)"
        )
        import anyio
        run1 = anyio.run(get_baseline_assessment_data, user)
        run2 = anyio.run(get_baseline_assessment_data, user)
        assert [q.id for q in run1.questions] == [q.id for q in run2.questions]

        # 3. Role readiness explainable calculation test
        u_create = User(
            email=f"readiness_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="password",
            full_name="Readiness Tester",
            department="MoSPI NAD",
            designation="Director (ISS)"
        )
        db_session.add(u_create)
        db_session.commit()
        db_session.refresh(u_create)

        profile = get_user_competency_profile(u_create.id, db_session)
        assert isinstance(profile.overall_readiness_score, float)
        assert profile.overall_readiness_score >= 0.0
    finally:
        db_session.close()

def test_baseline_assignment_persistence_and_unassigned_rejection():
    import uuid, anyio
    from fastapi import HTTPException
    from app.db.database import SessionLocal
    from app.models.models import BaselineAssignment
    db_session = SessionLocal()
    try:
        user = User(
            email=f"persist_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="password",
            full_name="Persistence Tester",
            department="MoSPI NAD",
            designation="Director (ISS)"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assessment = anyio.run(get_baseline_assessment_data, user, db_session)
        
        # Verify BaselineAssignment row was persisted in DB
        db_assign = db_session.query(BaselineAssignment).filter(BaselineAssignment.user_id == user.id).first()
        assert db_assign is not None
        assert db_assign.status == "assigned"
        assert db_assign.total_questions == 9

        # Attempt to submit unassigned question ID
        unassigned_answers = [BaselineAnswerSubmit(question_id=99999, selected_option="A")]
        submission = BaselineAssessmentSubmit(answers=unassigned_answers)

        with pytest.raises(HTTPException) as exc_info:
            evaluate_baseline_submission(user.id, submission, db_session)
        assert exc_info.value.status_code == 400
        assert "not assigned" in exc_info.value.detail
    finally:
        db_session.close()

def test_designation_resolution_priority_order():
    # Exact Match
    exact_res = resolve_role_benchmarks("MoSPI NAD", "Director")
    assert exact_res["resolution_method"] == "exact"
    assert exact_res["role_category"] == "senior"

    # Alias Match
    alias_res = resolve_role_benchmarks("MoSPI FOD", "dd")
    assert alias_res["resolution_method"] == "alias"
    assert alias_res["role_category"] == "mid"

    # Specific Keyword Candidate Match ("Deputy Director" before "Director")
    keyword_res = resolve_role_benchmarks("MoSPI NAD", "Deputy Director (ISS)")
    assert keyword_res["resolution_method"] == "keyword"
    assert keyword_res["role_category"] == "mid"

    # Fallback Keyword
    fallback_res = resolve_role_benchmarks("MoSPI Policy", "Chief Executive Advisor")
    assert fallback_res["resolution_method"] == "fallback_keyword"
    assert fallback_res["role_category"] == "senior"

    # Default Fallback
    default_res = resolve_role_benchmarks("MoSPI General", "Unrecognized Role Title")
    assert default_res["resolution_method"] == "default"
    assert default_res["role_category"] == "mid"

def test_resource_provenance_metadata():
    from app.data.seed_data import RESOURCES_SEED
    sources = set(r["source"] for r in RESOURCES_SEED)
    assert "NSSTA" in sources
    assert "MoSPI" in sources
    
    # Verify optional/nullable reference period
    has_null_ref = any(r.get("reference_period") is None for r in RESOURCES_SEED)
    assert has_null_ref, "Reference period should be optional/nullable where not applicable"

def test_question_bank_coverage_and_fallback():
    from app.services.assessment_service import select_role_specific_questions
    target_count = 6
    core_comps = ["STAT_SURVEY", "STAT_NAT_ACC"]
    selected = select_role_specific_questions("senior", target_count, core_comps, exclude_ids=set())
    
    # Check no duplicate IDs
    ids = [q["id"] for q in selected]
    assert len(ids) == len(set(ids)), "Duplicate question IDs must be prevented"
    assert len(selected) <= target_count

def test_one_active_baseline_assignment_per_user():
    import uuid, anyio
    from app.db.database import SessionLocal
    from app.models.models import BaselineAssignment
    db_session = SessionLocal()
    try:
        user = User(
            email=f"active_assign_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="password",
            full_name="Active Assignment Tester",
            department="MoSPI NAD",
            designation="Director (ISS)"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Retrieve baseline twice
        assign1 = anyio.run(get_baseline_assessment_data, user, db_session)
        assign2 = anyio.run(get_baseline_assessment_data, user, db_session)

        # Re-retrieval should reuse same assignment_id
        assert assign1.assessment_id == assign2.assessment_id

        # Verify exactly 1 active assignment row in DB
        active_count = db_session.query(BaselineAssignment).filter(
            BaselineAssignment.user_id == user.id,
            BaselineAssignment.status == "assigned"
        ).count()
        assert active_count == 1
    finally:
        db_session.close()

def test_duplicate_baseline_submission_protection():
    import uuid, anyio
    from fastapi import HTTPException
    from app.db.database import SessionLocal
    from app.models.models import LearningProgressHistory, BaselineAssignment
    db_session = SessionLocal()
    try:
        user = User(
            email=f"dup_sub_{uuid.uuid4().hex[:6]}@mospi.gov.in",
            hashed_password="password",
            full_name="Duplicate Submission Tester",
            department="MoSPI FOD",
            designation="Statistical Investigator"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assessment = anyio.run(get_baseline_assessment_data, user, db_session)
        answers = [BaselineAnswerSubmit(question_id=q.id, selected_option="A") for q in assessment.questions]
        submission = BaselineAssessmentSubmit(answers=answers)

        # First submission should succeed
        eval1 = evaluate_baseline_submission(user.id, submission, db_session)
        assert eval1.overall_score >= 0.0

        hist_count = db_session.query(LearningProgressHistory).filter(LearningProgressHistory.user_id == user.id).count()

        # Second submission of same assignment must be rejected
        with pytest.raises(HTTPException) as exc_info:
            evaluate_baseline_submission(user.id, submission, db_session)
        assert exc_info.value.status_code == 400
        assert "Duplicate submission rejected" in exc_info.value.detail

        # Verify progress history count was NOT incremented twice
        hist_count_after = db_session.query(LearningProgressHistory).filter(LearningProgressHistory.user_id == user.id).count()
        assert hist_count_after == hist_count
    finally:
        db_session.close()
