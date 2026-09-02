import pytest
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Competency, UserCompetency, QuizAttempt, LearningProgressHistory
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def admin_user():
    db = SessionLocal()
    u = User(
        email=f"admin_analytics_{uuid.uuid4().hex[:6]}@mospi.gov.in",
        hashed_password="hash",
        full_name="Chief Analytics Admin",
        designation="Director General",
        department="National Accounts Division",
        role="admin"
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    token = create_access_token({"sub": str(u.id)})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()
    return u, headers

@pytest.fixture
def officer_user():
    db = SessionLocal()
    u = User(
        email=f"officer_analytics_{uuid.uuid4().hex[:6]}@mospi.gov.in",
        hashed_password="hash",
        full_name="Field Officer",
        designation="Statistical Investigator",
        department="Field Operations Division",
        role="officer"
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    token = create_access_token({"sub": str(u.id)})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()
    return u, headers

def test_admin_analytics_authorization(admin_user):
    admin, headers = admin_user
    endpoints = [
        "/api/v1/admin/analytics/overview",
        "/api/v1/admin/analytics/competencies",
        "/api/v1/admin/analytics/departments",
        "/api/v1/admin/analytics/training-effectiveness",
        "/api/v1/admin/analytics/skill-gaps",
        "/api/v1/admin/analytics/emerging-skills",
        "/api/v1/admin/analytics/capacity-forecast",
    ]
    for ep in endpoints:
        res = client.get(ep, headers=headers)
        assert res.status_code == 200, f"Failed for endpoint {ep}: {res.text}"

def test_non_admin_analytics_rejection(officer_user):
    officer, headers = officer_user
    endpoints = [
        "/api/v1/admin/analytics/overview",
        "/api/v1/admin/analytics/competencies",
        "/api/v1/admin/analytics/departments",
        "/api/v1/admin/analytics/training-effectiveness",
        "/api/v1/admin/analytics/skill-gaps",
        "/api/v1/admin/analytics/emerging-skills",
        "/api/v1/admin/analytics/capacity-forecast",
    ]
    for ep in endpoints:
        res = client.get(ep, headers=headers)
        assert res.status_code == 403, f"Non-admin should be rejected with 403 for {ep}"

def test_workforce_competency_aggregation(admin_user):
    admin, headers = admin_user

    # Overview endpoint
    res_ov = client.get("/api/v1/admin/analytics/overview", headers=headers)
    assert res_ov.status_code == 200
    ov = res_ov.json()
    assert ov["total_officers"] >= 1
    assert "organization_readiness_score" in ov
    assert "evidence_level" in ov
    assert ov["calculation_method"] != ""

    # Competencies endpoint
    res_comp = client.get("/api/v1/admin/analytics/competencies", headers=headers)
    assert res_comp.status_code == 200
    comps = res_comp.json()
    assert len(comps["competencies"]) > 0
    first_c = comps["competencies"][0]
    assert "code" in first_c
    assert "average_gap" in first_c
    assert "priority_rank" in first_c

def test_department_and_role_tier_breakdown(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/departments", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "departments" in data
    assert "role_tiers" in data
    assert len(data["departments"]) > 0

def test_training_effectiveness_metrics(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/training-effectiveness", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["data_status"] in ["VALID", "INSUFFICIENT_DATA"]
    assert "completion_rate_pct" in data
    assert "average_quiz_score" in data
    assert "average_competency_gain" in data

def test_skill_gap_intelligence_priority_formula(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/skill-gaps", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["top_critical_gaps"]) > 0
    top_gap = data["top_critical_gaps"][0]
    assert "priority_score" in top_gap
    assert "formula_explanation" in top_gap
    assert "Priority Score =" in data["priority_formula"]

def test_emerging_skills_rule_based_signals(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/emerging-skills", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["signals"]) > 0
    sig = data["signals"][0]
    assert sig["signal_status"] in ["EMERGING", "GROWING", "STABLE", "INSUFFICIENT_DATA"]
    assert sig["evidence_rationale"] != ""

def test_capacity_forecast_assumptions_transparency(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/capacity-forecast", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "forecast_status" in data
    assert "assumptions" in data
    assert len(data["assumptions"]) > 0
    assert "projected_readiness_60d" in data

def test_privacy_preservation_no_sensitive_text_leakage(admin_user):
    admin, headers = admin_user
    res = client.get("/api/v1/admin/analytics/overview", headers=headers)
    data_str = str(res.json())
    # Ensure no raw chat content or private keys are exposed
    assert "hashed_password" not in data_str
    assert "chat_messages" not in data_str

def test_backward_compatibility_with_all_phases(officer_user):
    officer, headers = officer_user
    # Profile check from Phase 1
    p_res = client.get("/api/v1/auth/me", headers=headers)
    assert p_res.status_code == 200

    # Gap analysis from Phase 2
    gap_res = client.get("/api/v1/competencies/gap-analysis", headers=headers)
    assert gap_res.status_code == 200

    # Chat session from Phase 5B
    chat_res = client.post("/api/v1/chat/sessions", json={"title": "Regression Check"}, headers=headers)
    assert chat_res.status_code == 201
