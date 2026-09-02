# AI-Enabled Role-Based Skills Intelligence & Capacity Building Platform for India's Official Statistical System

> **MoSPI • NSSTA • iGOT Karmayogi Official Capacity Building Ecosystem**  
> Tailored for officers across the Ministry of Statistics and Programme Implementation (MoSPI), National Statistical Systems Training Academy (NSSTA), State Directorates of Economics & Statistics (DES), and Indian Statistical Service (ISS / SSS) cadres.

---

## 🌟 Executive Overview & Core Capabilities

The **AI-Enabled Role-Based Skills Intelligence & Capacity Building Platform** is an enterprise-grade, evidence-driven capacity building system designed specifically for India's Official Statistical System.

### Key Capabilities

1. **Role & Designation-Based Competency Mapping**:
   - Mapped across 9 official statistical domains (National Accounts, Survey Methodology, Index Numbers, Labour Statistics, Data Science, etc.).
   - Tailored benchmark expectations for Senior (ISS Officers, Directors), Mid-level (Deputy Directors, Assistant Directors), and Technical (Statistical Investigators, Field Surveyors) cadres.

2. **Common Core + Role-Specific Baseline Assessment**:
   - 9-question baseline assessment (5 Common Core + 4 Role-Specific) providing an immediate, objective competency initialization.

3. **Continuous Adaptive Learning Loop**:
   - Recalculates competency profiles upon verified activity evidence (quizzes, resource completions) with diminishing returns and mathematical gain caps (0.0 to 100.0%).

4. **Official Learning Ecosystem Integration**:
   - Integrates 4 official government learning providers: **iGOT Karmayogi**, **NSSTA TPAC**, **MoSPI Official Publications**, and **eSankhyiki Datasets**.
   - Preserves explicit provenance metadata (`Live Official API`, `Live Official Metadata`, `Curated Official Metadata`) and verification levels (`PORTAL_VERIFIED`, `RESOURCE_VERIFIED`, `UNVERIFIED`).

5. **AI-Powered Content Processing & Assessment Studio**:
   - Secure document ingestion (PDF, DOCX, PPTX, TXT) with SHA-256 deduplication and structural text chunking (`ContentChunk`).
   - Schema-enforced AI quiz generation with strict deterministic fallback when external LLM APIs are unconfigured.

6. **AI-Powered Conversational Virtual Assistant (RAG Chat)**:
   - Personalized assistant providing contextual guidance using officer competency profiles and document chunk RAG retrieval.
   - Enforces strict cross-user document and session isolation (`Document.user_id == current_user.id`).

7. **Advanced Workforce Analytics & Predictive Insights**:
   - Admin intelligence dashboards providing organization-wide readiness scores, department/tier gap breakdowns, training completion rates, and ranked critical gaps.
   - Rule-based emerging skill trend signals (`EMERGING`, `GROWING`, `STABLE`, `INSUFFICIENT_DATA`).
   - Conservative capacity-building forecasts based on empirical historical gain rates with explicit assumptions and mathematical capping disclaimers.

8. **Production Security & Hardening**:
   - Robust JWT authentication, RBAC enforcement (`admin` vs `officer`), non-admin HTTP 403 rejection, and identity spoofing protection.

---

## 📋 SIH Requirement Traceability Matrix

| SIH Requirement | Implemented Platform Feature | Status | Evidence / Verification |
| :--- | :--- | :--- | :--- |
| **1. AI-Based Competency Assessment** | Common Core + Role-Specific Baseline Engine | `IMPLEMENTED` | Tested in `test_designation_baseline.py` & Step 5-6 of `verify_e2e.py` |
| **2. Automated Skill-Gap Analysis** | Role Benchmark Gap Calculation & Priority Engine | `IMPLEMENTED` | Tested in `test_competency.py` & Step 7 of `verify_e2e.py` |
| **3. Personalized Learning Recommendations** | Role & Gap Mapped Recommendation Engine | `IMPLEMENTED` | Tested in `test_official_resource_integration.py` & Step 10 of `verify_e2e.py` |
| **4. iGOT Karmayogi Integration** | Provider Adapter (FRAC Taxonomy Mapped) | `INTEGRATION_READY` | Fallback mode active; `REQUIRES_EXTERNAL_CREDENTIALS` for Live API |
| **5. NSSTA TPAC Training Recommendations** | NSSTA TPAC Training Adapter & Sync | `IMPLEMENTED` | Tested in `test_official_learning_ecosystem.py` & Step 9 of `verify_e2e.py` |
| **6. Official Statistical Resources** | MoSPI Technical Manuals & eSankhyiki Hub | `IMPLEMENTED` | Tested in `test_official_resource_integration.py` & Step 9-10 of `verify_e2e.py` |
| **7. Adaptive Learning Cycle** | Continuous Adaptive Loop & Diminishing Returns | `IMPLEMENTED` | Tested in `test_adaptive_learning_loop.py` & Step 10b of `verify_e2e.py` |
| **8. AI MCQ Generation** | Multi-Provider LLM & Deterministic Fallback Generator | `IMPLEMENTED` | Tested in `test_ai_mcq_generator.py` & Step 11 of `verify_e2e.py` |
| **9. Quiz Generation & Evaluation** | Quiz Examination Engine & Competency Recalibration | `IMPLEMENTED` | Tested in `test_phase4_assessment_content.py` & Step 12-13 of `verify_e2e.py` |
| **10. Document Assessment Processing** | Document Ingestion (PDF/TXT), Extraction & Chunking | `IMPLEMENTED` | Tested in `test_document_upload_security.py` & Step 10 of `verify_e2e.py` |
| **11. Personalized Learning Feedback** | Qualitative Pedagogical Feedback & Roadmap Generator | `IMPLEMENTED` | Tested in `test_phase4_assessment_content.py` & Step 14-15 of `verify_e2e.py` |
| **12. Virtual AI Assistant** | RAG Chat Engine & Competency Context Personalization | `IMPLEMENTED` | Tested in `test_phase5b_virtual_assistant.py` & Step 21 of `verify_e2e.py` |
| **13. Interactive Learner Intelligence APIs** | REST Endpoint Suite for Profiles, Gaps & Path | `IMPLEMENTED` | Tested across all backend routers |
| **14. Administrator Analytics** | Workforce Overview, Competencies & Dept Breakdown | `IMPLEMENTED` | Tested in `test_phase6_workforce_analytics.py` & Step 20, 22 of `verify_e2e.py` |
| **15. Training Effectiveness Analytics** | Verified Gain Deltas & Before vs After Progression | `IMPLEMENTED` | Tested in `test_phase6_workforce_analytics.py` & Step 22 of `verify_e2e.py` |
| **16. Emerging Skill Intelligence** | Rule-Based Signal Detection (`EMERGING`, `GROWING`, etc.) | `IMPLEMENTED` | Tested in `test_phase6_workforce_analytics.py` & Step 22 of `verify_e2e.py` |
| **17. Capacity-Building Forecasting** | Empirical Extrapolation Model & Capping Disclaimers | `IMPLEMENTED` | Tested in `test_phase6_workforce_analytics.py`, `test_phase7` & Step 22-23 |
| **18. Role-Based Access Control** | Token Auth & Admin RBAC Guard (`HTTP 403`) | `IMPLEMENTED` | Tested in `test_admin_auth.py`, `test_phase7` & Step 19, 23 of `verify_e2e.py` |
| **19. Secure API Architecture** | SHA-256 Deduplication, Input Validation & Isolation | `IMPLEMENTED` | Tested in `test_phase7_final_hardening.py` |
| **20. Cloud-Ready & Interoperable** | Modular FastApi Service & Provider Adapter Architecture | `IMPLEMENTED` | Verified via 103 unit tests & 23 E2E checks |

---

## 🏗 System Architecture

```
                                ┌───────────────────────────────────────────────┐
                                │           React 18 + Vite Frontend            │
                                │      (Tailwind CSS, Recharts, Lucide)         │
                                └───────────────────────┬───────────────────────┘
                                                        │ REST API / JWT
                                                        ▼
                                ┌───────────────────────────────────────────────┐
                                │             FastAPI Backend Engine            │
                                │        (Pydantic v2, SQLAlchemy 2.0)          │
                                └───────┬───────────────┬───────────────┬───────┘
                                        │               │               │
               ┌────────────────────────┴─┐   ┌─────────┴─────────┐   ┌─┴────────────────────────┐
               ▼                          ▼   ▼                   ▼   ▼                          ▼
        [Relational DB]                [AI Engine]         [Document Parser]        [Govt Resource Hub]
     Users, Competencies,             Multi-Provider      PDF, DOCX, PPTX, TXT      iGOT Karmayogi (FRAC),
     Assessments, Quizzes,            (Grok / Gemini /    Extraction & Chunking     NSSTA Greater Noida,
     Chat, Workforce Analytics        OpenAI / Fallback)   (SHA-256 Hash Check)     MoSPI & eSankhyiki
```

---

## 🛠 Technology Stack

- **Backend Framework**: Python 3.11+ / 3.14, FastAPI, Uvicorn
- **Data Validation & Schemas**: Pydantic v2
- **Database & ORM**: SQLite / PostgreSQL, SQLAlchemy 2.0
- **Security & Authentication**: PyJWT / python-jose, Passlib / bcrypt
- **LLM Integrations**: Multi-provider architecture (Google Gemini, Grok/xAI, OpenAI, Deterministic Fallback)
- **Frontend Framework**: React 18, Vite, Tailwind CSS, Recharts, Lucide Icons

---

## 🚀 Installation & Execution

### Prerequisites
- Python 3.11+ (Compatible with Python 3.14)
- Node.js v18+

### 1. Backend Setup
```bash
# Navigate to workspace root
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run FastAPI development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## ⚙️ Environment Variables Guide

Copy `.env.example` to `.env` in the root directory:

| Variable Name | Description | Default / Example Value |
| :--- | :--- | :--- |
| `SECRET_KEY` | JWT signing secret key | `mospi-secret-key-production-change-me` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_EXPIRETIME_MINUTES` | Access token expiration | `1440` (24 hours) |
| `DATABASE_URL` | SQLite / PostgreSQL URI | `sqlite:///./app.db` |
| `GEMINI_API_KEY` | Google Gemini API Key | `AIzaSy...` (Optional, fallback active) |
| `GROK_API_KEY` | Grok / xAI API Key | `xai-...` (Optional, fallback active) |
| `IGOT_API_KEY` | iGOT Karmayogi API Key | `igot-...` (Optional, fallback active) |

---

## 🧪 Testing & Verification

### Running Unit Tests (`pytest`)
Run the complete test suite (103 unit tests covering Phases 1–7):
```bash
python -m pytest
```

### Running End-to-End System Verification (`verify_e2e.py`)
Run the complete 23-stage E2E capabilities verification script:
```bash
python verify_e2e.py
```

Expected output:
```text
================================================================
ALL 23 END-TO-END CAPABILITY CHECKS PASSED WITH 100% SUCCESS!
================================================================
```

---

## 🔒 Security & Privacy Features

1. **Strict User Isolation**: All personal officer records (chat sessions, uploaded documents, assessment attempts, learning history) are strictly bound to `current_user.id`.
2. **Identity Spoofing Prevention**: User identity is derived exclusively from the validated JWT token (`sub` claim); client-supplied query params or body fields cannot override identity.
3. **Role-Based Access Control (RBAC)**: Non-admin users attempting to access `/api/v1/admin/*` endpoints receive an immediate `HTTP 403 Forbidden` response.
4. **No Secrets Leakage**: Internal passwords, JWT secrets, and database connection strings are filtered out of API output schemas.
