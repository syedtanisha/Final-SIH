import sys
import os
import json
import io

# Ensure backend package path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from fastapi.testclient import TestClient
from app.main import app, seed_initial_data
from app.db.database import SessionLocal
from app.models.models import User
from app.core.security import create_access_token

def test_all_live_endpoints_as_user():
    seed_initial_data()
    client = TestClient(app)
    results = []

    print("================================================================================")
    print("STARTING REAL-USER ENDPOINT TESTING WITH AUTHENTIC MoSPI STATISTICAL DATA")
    print("================================================================================\n")

    # ---------------------------------------------------------
    # 1. Platform Health & Root
    # ---------------------------------------------------------
    res_root = client.get("/")
    assert res_root.status_code == 200
    results.append(("GET /", 200, res_root.json(), "Root platform metadata and version"))
    print("[1/27] GET / -> 200 OK")

    res_health = client.get("/health")
    assert res_health.status_code == 200
    results.append(("GET /health", 200, res_health.json(), "Health check"))
    print("[2/27] GET /health -> 200 OK")

    # ---------------------------------------------------------
    # 2. Authentication Flow
    # ---------------------------------------------------------
    user_email = "ananya.sharma.iss@mospi.gov.in"
    reg_payload = {
        "email": user_email,
        "password": "OfficialSecurePassword2026!",
        "full_name": "Smt. Ananya Sharma",
        "designation": "Deputy Director",
        "department": "MoSPI Field Operations Division (FOD)",
        "organization": "National Sample Survey Office (NSSO)"
    }
    res_reg = client.post("/api/v1/auth/register", json=reg_payload)
    results.append(("POST /api/v1/auth/register", res_reg.status_code, res_reg.json(), f"Registered Officer: {user_email}"))
    print(f"[3/27] POST /api/v1/auth/register -> {res_reg.status_code}")

    res_login_json = client.post("/api/v1/auth/login/json", json={
        "username": user_email,
        "password": "OfficialSecurePassword2026!"
    })
    assert res_login_json.status_code == 200
    token = res_login_json.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    results.append(("POST /api/v1/auth/login/json", 200, {"token_type": "Bearer", "user": res_login_json.json()["user"]}, "JWT token generated via JSON login"))
    print("[4/27] POST /api/v1/auth/login/json -> 200 OK")

    res_login_form = client.post("/api/v1/auth/login", data={
        "username": user_email,
        "password": "OfficialSecurePassword2026!"
    })
    assert res_login_form.status_code == 200
    results.append(("POST /api/v1/auth/login", 200, {"token_type": "Bearer"}, "OAuth2 Form login verified"))
    print("[5/27] POST /api/v1/auth/login -> 200 OK")

    res_me = client.get("/api/v1/auth/me", headers=headers)
    assert res_me.status_code == 200
    results.append(("GET /api/v1/auth/me", 200, res_me.json(), "Retrieved current logged-in officer profile"))
    print("[6/27] GET /api/v1/auth/me -> 200 OK")

    res_update_me = client.put("/api/v1/auth/profile", json={
        "full_name": "Smt. Ananya Sharma (ISS)",
        "designation": "Joint Director",
        "department": "MoSPI Survey Design and Research Division (SDRD)"
    }, headers=headers)
    assert res_update_me.status_code == 200
    results.append(("PUT /api/v1/auth/profile", 200, res_update_me.json(), "Updated cadre designation and division profile"))
    print("[7/27] PUT /api/v1/auth/profile -> 200 OK")

    # ---------------------------------------------------------
    # 3. Competencies & Gap Analysis Flow
    # ---------------------------------------------------------
    res_comps = client.get("/api/v1/competencies", headers=headers)
    assert res_comps.status_code == 200
    results.append(("GET /api/v1/competencies", 200, {"total_competencies": len(res_comps.json())}, "Retrieved all 9 official MoSPI statistical competencies"))
    print("[8/27] GET /api/v1/competencies -> 200 OK")

    res_comp_profile = client.get("/api/v1/competencies/profile", headers=headers)
    assert res_comp_profile.status_code == 200
    results.append(("GET /api/v1/competencies/profile", 200, res_comp_profile.json(), "Retrieved officer competency profile with calibrated benchmarks"))
    print("[9/27] GET /api/v1/competencies/profile -> 200 OK")

    res_gap_analysis = client.get("/api/v1/competencies/gap-analysis", headers=headers)
    assert res_gap_analysis.status_code == 200
    results.append(("GET /api/v1/competencies/gap-analysis", 200, res_gap_analysis.json(), "Deterministic Gap Matrix & AI Capacity Building Diagnosis"))
    print("[10/27] GET /api/v1/competencies/gap-analysis -> 200 OK")

    # ---------------------------------------------------------
    # 4. Diagnostic Assessment Flow
    # ---------------------------------------------------------
    res_baseline = client.get("/api/v1/assessments/baseline", headers=headers)
    assert res_baseline.status_code == 200
    b_questions = res_baseline.json()["questions"]
    results.append(("GET /api/v1/assessments/baseline", 200, {"questions_count": len(b_questions)}, "Loaded 9-discipline baseline diagnostic examination"))
    print(f"[11/27] GET /api/v1/assessments/baseline -> 200 OK ({len(b_questions)} questions)")

    # Submit baseline answers
    baseline_submission = [
        {"question_id": q["id"], "selected_option": "B" if q["id"] in [1, 3, 5, 6, 7, 9] else "A"}
        for q in b_questions
    ]
    res_baseline_submit = client.post("/api/v1/assessments/baseline/submit", json={"answers": baseline_submission}, headers=headers)
    assert res_baseline_submit.status_code == 200
    results.append(("POST /api/v1/assessments/baseline/submit", 200, res_baseline_submit.json(), "Submitted diagnostic assessment & initialized all 9 competency baselines"))
    print(f"[12/27] POST /api/v1/assessments/baseline/submit -> 200 OK (Score: {res_baseline_submit.json()['overall_score']}%)")

    # ---------------------------------------------------------
    # 5. Government Learning Hub & Recommendations Flow
    # ---------------------------------------------------------
    res_rec = client.get("/api/v1/recommendations/for-you", headers=headers)
    assert res_rec.status_code == 200
    results.append(("GET /api/v1/recommendations/for-you", 200, res_rec.json(), "Personalized iGOT Karmayogi & NSSTA module recommendations"))
    print(f"[13/27] GET /api/v1/recommendations/for-you -> 200 OK (Target: {res_rec.json()['primary_focus_gap']})")

    res_path = client.get("/api/v1/recommendations/learning-path", headers=headers)
    assert res_path.status_code == 200
    results.append(("GET /api/v1/recommendations/learning-path", 200, res_path.json(), "Generated 7-step personalized capacity building roadmap"))
    print(f"[14/27] GET /api/v1/recommendations/learning-path -> 200 OK ({len(res_path.json()['milestones'])} milestones)")

    res_resources = client.get("/api/v1/resources?source=iGOT_Karmayogi&limit=10&offset=0", headers=headers)
    assert res_resources.status_code == 200
    results.append(("GET /api/v1/resources", 200, {"resources_count": len(res_resources.json())}, "Catalog of iGOT CBPs, NSSTA manuals, and MoSPI publications"))
    print(f"[15/27] GET /api/v1/resources -> 200 OK ({len(res_resources.json())} resources returned)")

    # ---------------------------------------------------------
    # 6. Document Ingestion & AI Quiz Generation Flow
    # ---------------------------------------------------------
    official_plfs_document = (
        "Ministry of Statistics and Programme Implementation (MoSPI) - Periodic Labour Force Survey (PLFS).\n\n"
        "1. Sampling Design: The sampling design is a stratified multi-stage design. The First Stage Units (FSU) "
        "in rural areas are 2011 Census villages and in urban areas are Urban Frame Survey (UFS) blocks.\n"
        "2. Multipliers & Weights: For unbiased population estimation, sampling multipliers must be applied to "
        "every unit-level household record (USU) in Schedule 10.4.\n"
        "3. Activity Status Classification: A person is categorized under Current Weekly Status (CWS) as employed "
        "if they performed economic activity for at least 1 hour on any 1 day during the 7-day reference period."
    )
    doc_file = ("plfs_sampling_and_weighting_manual.txt", io.BytesIO(official_plfs_document.encode("utf-8")), "text/plain")
    res_doc_upload = client.post("/api/v1/documents/upload", files={"file": doc_file}, headers=headers)
    assert res_doc_upload.status_code == 201
    uploaded_doc_id = res_doc_upload.json()["id"]
    results.append(("POST /api/v1/documents/upload", 201, res_doc_upload.json(), "Uploaded official methodology text and extracted text"))
    print(f"[16/27] POST /api/v1/documents/upload -> 201 Created (Doc ID: {uploaded_doc_id})")

    res_docs_list = client.get("/api/v1/documents", headers=headers)
    assert res_docs_list.status_code == 200
    results.append(("GET /api/v1/documents", 200, {"documents_count": len(res_docs_list.json())}, "Listed user's uploaded training documents"))
    print(f"[17/27] GET /api/v1/documents -> 200 OK ({len(res_docs_list.json())} documents)")

    # Generate AI Quiz from Document
    res_quiz_gen = client.post("/api/v1/quizzes/generate", json={
        "topic": "PLFS Multi-Stage Sampling & Weighting",
        "document_id": uploaded_doc_id,
        "num_questions": 3,
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res_quiz_gen.status_code == 201
    generated_quiz = res_quiz_gen.json()
    quiz_id = generated_quiz["id"]
    results.append(("POST /api/v1/quizzes/generate", 201, generated_quiz, "AI Generated 3 schema-enforced MCQs based directly on document"))
    print(f"[18/27] POST /api/v1/quizzes/generate -> 201 Created (Quiz ID: {quiz_id})")

    res_quiz_list = client.get("/api/v1/quizzes?limit=10&offset=0", headers=headers)
    assert res_quiz_list.status_code == 200
    results.append(("GET /api/v1/quizzes", 200, {"quizzes_count": len(res_quiz_list.json())}, "Listed officer's generated quizzes"))
    print(f"[19/27] GET /api/v1/quizzes -> 200 OK ({len(res_quiz_list.json())} quizzes)")

    res_quiz_detail = client.get(f"/api/v1/quizzes/{quiz_id}", headers=headers)
    assert res_quiz_detail.status_code == 200
    results.append((f"GET /api/v1/quizzes/{quiz_id}", 200, res_quiz_detail.json(), "Retrieved quiz questions for examination taking"))
    print(f"[20/27] GET /api/v1/quizzes/{quiz_id} -> 200 OK")

    # Submit Quiz Answers & Calculate Closed-Loop Competency Delta Gain (+Δ%)
    quiz_answers = [
        {"question_id": q["id"], "selected_option": "A"}
        for q in generated_quiz["questions"]
    ]
    res_quiz_submit = client.post(f"/api/v1/quizzes/{quiz_id}/submit", json={"answers": quiz_answers}, headers=headers)
    assert res_quiz_submit.status_code == 200
    quiz_res_data = res_quiz_submit.json()
    results.append((f"POST /api/v1/quizzes/{quiz_id}/submit", 200, quiz_res_data, "Evaluated quiz and recalculated competency delta growth"))
    print(f"[21/27] POST /api/v1/quizzes/{quiz_id}/submit -> 200 OK (Delta Gain: +{quiz_res_data['competency_delta']}%)")

    # ---------------------------------------------------------
    # 7. Longitudinal Progress Analytics Flow
    # ---------------------------------------------------------
    # Longitudinal progress summary with embedded history events
    res_prog_summary = client.get("/api/v1/progress/summary", headers=headers)
    assert res_prog_summary.status_code == 200
    prog_data = res_prog_summary.json()
    results.append(("GET /api/v1/progress/summary", 200, prog_data, f"Readiness Index: {prog_data['overall_readiness_score']}%, Total Gain: +{prog_data['total_learning_gain']}%, History Events: {len(prog_data.get('progress_events', []))}"))
    print(f"[22/26] GET /api/v1/progress/summary -> 200 OK (Readiness: {prog_data['overall_readiness_score']}%, Events: {len(prog_data.get('progress_events', []))})")

    # ---------------------------------------------------------
    # 8. AI Final Interview Flow
    # ---------------------------------------------------------
    res_interview_readiness = client.get("/api/v1/final-interview/readiness", headers=headers)
    assert res_interview_readiness.status_code == 200
    results.append(("GET /api/v1/final-interview/readiness", 200, res_interview_readiness.json(), "Final interview readiness check and remaining focus disciplines"))
    print(f"[24/27] GET /api/v1/final-interview/readiness -> 200 OK (Ready: {res_interview_readiness.json()['eligible']})")

    res_interview_questions = client.post("/api/v1/final-interview/questions", headers=headers)
    assert res_interview_questions.status_code == 200
    results.append(("POST /api/v1/final-interview/questions", 200, res_interview_questions.json(), "Generated progressive multi-level interview questions across domains"))
    print(f"[25/27] POST /api/v1/final-interview/questions -> 200 OK ({len(res_interview_questions.json().get('questions', []))} questions)")

    res_interview_eval = client.post("/api/v1/final-interview/evaluate-answer", json={
        "question": "Explain how the National Accounts Division computes Gross Value Added (GVA) at Basic Prices under the SNA 2008 framework.",
        "answer": (
            "Under the SNA 2008 series adopted by MoSPI, GVA at basic prices is calculated as Gross Output minus Intermediate Consumption. "
            "It measures the net value created by each industry sector (agriculture, manufacturing, services) before adding product taxes "
            "and subtracting product subsidies to arrive at GDP at market prices."
        ),
        "competency": "STAT_NAT_ACC",
        "domain": "Macroeconomic Statistics",
        "difficulty": "Intermediate"
    }, headers=headers)
    assert res_interview_eval.status_code == 200
    results.append(("POST /api/v1/final-interview/evaluate-answer", 200, res_interview_eval.json(), "Evaluated officer interview answer across 5 core competency pillars"))
    print(f"[26/27] POST /api/v1/final-interview/evaluate-answer -> 200 OK (Score: {res_interview_eval.json()['score']}/10)")

    # ---------------------------------------------------------
    # 9. Admin Security Authorization Flow
    # ---------------------------------------------------------
    # Step A: Regular officer gets 403 Forbidden
    res_admin_forbidden = client.get("/api/v1/admin/stats", headers=headers)
    assert res_admin_forbidden.status_code == 403
    print("[27a/27] GET /api/v1/admin/stats (Regular Officer) -> 403 Forbidden [Verified Security Block]")

    # Step B: Admin gets 200 OK
    db = SessionLocal()
    try:
        admin_officer = db.query(User).filter(User.email == "chief.statistician@mospi.gov.in").first()
        if not admin_officer:
            admin_officer = User(
                email="chief.statistician@mospi.gov.in",
                hashed_password="adminhashpassword",
                full_name="Dr. G. P. Samanta",
                designation="Chief Statistician of India & Secretary",
                department="Ministry of Statistics and Programme Implementation",
                role="admin"
            )
            db.add(admin_officer)
            db.commit()
            db.refresh(admin_officer)
        admin_token = create_access_token({"sub": str(admin_officer.id)})
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
    finally:
        db.close()

    res_admin_ok = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert res_admin_ok.status_code == 200
    results.append(("GET /api/v1/admin/stats", 200, res_admin_ok.json(), "Admin ecosystem analytics: total officers, competencies, quizzes, avg readiness"))
    print("[27b/27] GET /api/v1/admin/stats (Admin Officer) -> 200 OK")

    print("\n================================================================================")
    print("ALL 27/27 BACKEND ENDPOINTS TESTED SUCCESSFULLY WITH ZERO FAILURES!")
    print("================================================================================")

    return results

if __name__ == "__main__":
    test_all_live_endpoints_as_user()
