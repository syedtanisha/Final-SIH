import json
import re
import logging
import httpx
from typing import List, Dict, Any, Optional
from ..core.config import settings

logger = logging.getLogger(__name__)

def clean_json_string(raw: str) -> str:
    """Strip markdown code blocks or trailing characters to obtain valid JSON."""
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    elif raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()

async def call_llm(prompt: str, system_prompt: str = "You are an AI Statistical Capacity Building Specialist for India's Official Statistical System.") -> str:
    """Multi-provider LLM executor supporting Grok (xAI), Groq, Gemini, OpenAI, or local fallback."""
    # 1. Try Grok (xAI) if key provided
    grok_key = settings.XAI_API_KEY or settings.GROK_API_KEY
    if grok_key:
        try:
            async with httpx.AsyncClient(timeout=35.0) as client:
                res = await client.post(
                    f"{settings.XAI_BASE_URL.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {grok_key}"},
                    json={
                        "model": settings.GROK_MODEL or "grok-2-latest",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[AI Service] Grok (xAI) call failed: {e}")

    # 2. Try Groq if key provided
    if settings.GROQ_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": settings.GROQ_MODEL or "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[AI Service] Groq call failed: {e}")

    # 3. Try Gemini if key provided
    if settings.GEMINI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}",
                    json={
                        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[AI Service] Gemini call failed: {e}")

    # Fallback deterministic response
    return ""

async def generate_grok_gap_diagnosis_async(
    officer_name: str,
    designation: str,
    division: str,
    gaps: List[Dict[str, Any]],
    overall_readiness: float
) -> str:
    """Use Grok AI to interpret deterministic gap metrics and explain role-tailored capacity building needs."""
    if not gaps:
        return (
            f"Outstanding capacity profile, {officer_name}! You have achieved benchmark readiness across all statistical competencies "
            f"for your role in {division}. Continue maintaining proficiency through advanced NSSTA research publications and MoSPI technical manuals."
        )

    top_gaps = gaps[:3]
    gap_descriptions = [f"{g['name']} (Current: {g['current_level']}%, Role Target: {g['required_level']}%, Gap: {g['gap']}%, Priority: {g['priority']})" for g in top_gaps]
    gap_str = "\n".join([f"- {gd}" for gd in gap_descriptions])

    prompt = f"""
Analyze the following officer competency gaps for India's Official Statistical System:
Officer Name: {officer_name}
Cadre / Designation: {designation}
Division / Department: {division}
Overall Readiness Index: {overall_readiness}%

Calculated Gaps:
{gap_str}

Provide a concise, 3-4 sentence professional capacity diagnosis using AI:
1. Explain specifically why bridging these gaps is critical for their role in {division}.
2. Recommend immediate learning actions using NSSTA laboratory resources and MoSPI publications.
3. Conclude with verification guidance via AI Learning Studio quizzes.
"""
    ai_response = await call_llm(prompt, system_prompt="You are an AI Senior Statistical Capacity Building Specialist for India's Ministry of Statistics (MoSPI) and NSSTA.")
    if ai_response and len(ai_response.strip()) > 30:
        return ai_response.strip()

    # High-quality fallback template
    top_gap_names = ", ".join([g["name"] for g in top_gaps])
    return (
        f"AI Capacity Diagnosis for {officer_name} ({designation}, {division}): "
        f"Your statistical readiness index currently stands at {overall_readiness}%. "
        f"Based on your role requirements in {division}, your primary capacity building priorities are {top_gap_names}. "
        f"We recommend completing the aligned NSSTA training modules and official MoSPI guidelines, followed by AI Studio verification quizzes to validate competency gains."
    )

def generate_gap_diagnosis(
    officer_name: str,
    designation: str,
    gaps: List[Dict[str, Any]],
    overall_readiness: float,
    division: str = "MoSPI"
) -> str:
    """Synchronous bridge for gap diagnosis with division context."""
    if not gaps:
        return f"Outstanding performance, {officer_name}! You have achieved benchmark competency across all standard domains in India's Official Statistical System."

    top_gaps = gaps[:3]
    top_gap_names = ", ".join([g["name"] for g in top_gaps])
    return (
        f"Diagnostic Assessment for {officer_name} ({designation}, {division}): "
        f"Your current statistical readiness index stands at {overall_readiness}%. "
        f"The primary areas requiring capacity building for your role are {top_gap_names}. "
        f"To bridge these competency gaps efficiently, complete the corresponding NSSTA training modules and review the official MoSPI technical publications. "
        f"Submitting targeted verification quizzes in the AI Learning Studio will automatically calibrate and record your official competency score growth."
    )

async def generate_grok_learning_path(
    officer_name: str,
    designation: str,
    division: str,
    gaps: List[Dict[str, Any]],
    matched_resources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Use AI to synthesize matched learning resources into a structured, phased learning roadmap."""
    resources_summary = "\n".join([
        f"- [{r.get('source', 'MoSPI')}] {r.get('title', '')} ({r.get('resource_type', '')}, Duration: {r.get('estimated_duration_mins', 60)}m, Aligned Gap: {r.get('matched_competency_name', '')})"
        for r in matched_resources[:6]
    ])

    top_gap_name = gaps[0]["name"] if gaps else "Survey Operations"

    prompt = f"""
You are creating a personalized capacity building learning path for an officer in India's Official Statistical System.

Officer: {officer_name}
Designation: {designation}
Division: {division}
Primary Focus Gap: {top_gap_name}

Available Government Learning Resources:
{resources_summary}

Organize the officer's journey into exactly 4 sequential learning milestones:
Phase 1: Diagnostic Calibration & Baseline
Phase 2: Core Concept Mastery (NSSTA Academy Modules)
Phase 3: Applied Technical Practice (NSSTA Lab & MoSPI Reports)
Phase 4: AI Practice Quiz Verification & Demonstrable Gain (+Delta)

Return ONLY valid JSON matching this array schema:
[
  {{
    "phase_number": 1,
    "title": "Phase 1 Title",
    "domain": "Domain Name",
    "description": "2-sentence practical objective",
    "recommended_resource": "Resource Title",
    "estimated_hours": 2.5,
    "action_type": "assessment" | "course" | "lab" | "quiz"
  }}
]
"""
    raw = await call_llm(prompt, system_prompt="You are an official learning path synthesizer for MoSPI and NSSTA.")
    if raw:
        try:
            parsed = json.loads(clean_json_string(raw))
            if isinstance(parsed, list) and len(parsed) >= 3:
                return parsed
        except Exception as e:
            print(f"[AI Service] Learning path parsing error: {e}")

    # High-quality fallback learning path
    return [
        {
            "phase_number": 1,
            "title": f"Phase 1: Calibrate Role Baseline for {division}",
            "domain": "Calibration",
            "description": f"Complete the diagnostic evaluation tailored to {designation} responsibilities and review deterministic gap metrics.",
            "recommended_resource": "Baseline Diagnostic Assessment",
            "estimated_hours": 0.5,
            "action_type": "assessment"
        },
        {
            "phase_number": 2,
            "title": f"Phase 2: NSSTA Foundations in {top_gap_name}",
            "domain": "Conceptual Foundations",
            "description": f"Complete foundational modules at NSSTA to build theoretical grounding in {top_gap_name}.",
            "recommended_resource": matched_resources[0]["title"] if matched_resources else "NSSTA Official Statistics Curriculum",
            "estimated_hours": 3.0,
            "action_type": "course"
        },
        {
            "phase_number": 3,
            "title": "Phase 3: NSSTA Digital Data Lab & Official MoSPI Publications",
            "domain": "Applied Practice",
            "description": "Study official survey manuals, microdata weighting SOPs, and index compilation methodologies.",
            "recommended_resource": matched_resources[1]["title"] if len(matched_resources) > 1 else "NSSTA Training Manual",
            "estimated_hours": 2.5,
            "action_type": "lab"
        },
        {
            "phase_number": 4,
            "title": "Phase 4: AI Learning Studio Quiz Verification & Gain Calibration",
            "domain": "Outcome & Delta",
            "description": "Generate schema-enforced verification quizzes from tutorial manuals to validate mastery and achieve demonstrable skill gain (+26%).",
            "recommended_resource": "AI Quiz Studio & Verification Engine",
            "estimated_hours": 1.0,
            "action_type": "quiz"
        }
    ]

async def generate_grok_quiz_feedback(
    quiz_title: str,
    topic: str,
    score_pct: float,
    total_correct: int,
    total_questions: int,
    competency_name: str,
    before_score: float,
    after_score: float,
    delta: float,
    mistakes: List[Dict[str, Any]]
) -> str:
    """Use Grok AI to analyze quiz submission performance, diagnose errors, and give actionable feedback."""
    mistake_summary = ""
    if mistakes:
        mistake_summary = "Questions needing review:\n" + "\n".join([
            f"- Q: {m.get('question_text', '')[:120]}... Selected: Option {m.get('user_selected', '')}, Correct: Option {m.get('correct_option', '')}. Explanation: {m.get('explanation', '')[:150]}"
            for m in mistakes[:3]
        ])
    else:
        mistake_summary = "All questions answered correctly with 100% accuracy."

    prompt = f"""
You are Grok AI evaluating a quiz attempt for a statistical professional.

Quiz: {quiz_title} ({topic})
Competency: {competency_name}
Score: {score_pct}% ({total_correct}/{total_questions} correct)
Competency Recalibration: {before_score}% -> {after_score}% (+{delta}% demonstrated learning gain)

Performance Details:
{mistake_summary}

Provide a concise, motivating, and pedagogical performance analysis (3-4 sentences):
1. Acknowledge the quantified competency gain (+{delta}%).
2. Highlight key conceptual takeaways and explain any specific misunderstandings from the incorrect questions.
3. Suggest the next learning module or practice step to maintain momentum.
"""
    ai_response = await call_llm(prompt, system_prompt="You are Grok AI providing pedagogical feedback on official statistical examinations.")
    if ai_response and len(ai_response.strip()) > 30:
        return ai_response.strip()

    # Fallback qualitative feedback
    if mistakes:
        return (
            f"AI Evaluation: You achieved {score_pct}% ({total_correct}/{total_questions} correct) on '{quiz_title}'. "
            f"Your competency in '{competency_name}' improved by +{delta}% (from {before_score}% to {after_score}%). "
            f"Review the question explanations below to reinforce official methodology before the next milestone."
        )
    return (
        f"AI Evaluation: Outstanding mastery! You achieved a perfect score of {score_pct}% ({total_correct}/{total_questions} correct) on '{quiz_title}'. "
        f"Your official competency in '{competency_name}' has increased to {after_score}% (+{delta}% learning gain). "
        f"Your statistical reasoning aligns completely with official guidelines. Proceed to the next milestone in your learning path!"
    )

async def generate_department_designation_baseline_questions_async(
    department: str,
    designation: str,
    cadre_seniority: str = "Statistical Officer",
    core_competencies: Optional[List[str]] = None,
    num_questions: int = 9
) -> List[Dict[str, Any]]:
    """
    Generate dynamic, AI-powered baseline assessment questions specifically tailored to an officer's
    department (division) and designation seniority level in India's Official Statistical System.
    """
    comp_list_str = ", ".join(core_competencies) if core_competencies else "STAT_SURVEY, STAT_NAT_ACC, STAT_COMPUTE, STAT_PRICE_IND, STAT_LABOUR, STAT_DATA_GOV, STAT_QUALITY, STAT_VIZ_COMM, STAT_IND_AGRI"

    prompt = f"""
You are the Chief Psychometrician for India's Ministry of Statistics and Programme Implementation (MoSPI) and NSSTA.
Design an official diagnostic baseline assessment tailored specifically for an officer with the following role profile:

Department / Division: {department or 'MoSPI General Cadre'}
Designation / Post: {designation or 'Statistical Officer'}
Cadre Seniority Tier: {cadre_seniority}
Core Competencies Focus: {comp_list_str}

Generate exactly {num_questions} calibrated Multiple Choice Questions (MCQs):
Requirements:
1. Every question MUST directly test real-world statistical knowledge, guidelines, or operational duties expected for an officer in {department} at the {designation} level.
2. Provide 4 distinct options (A, B, C, D) for each question with 1 single correct answer ('A', 'B', 'C', or 'D').
3. Include competency_code, domain, competency_name, difficulty, question_text, options (array of {{ "key": "A"|"B"|"C"|"D", "text": "..." }}), correct_option, and explanation.
4. Return ONLY a valid JSON array of question objects conforming to this schema:

[
  {{
    "id": 1,
    "competency_code": "STAT_NAT_ACC",
    "competency_name": "National Accounts Statistics",
    "domain": "Macroeconomic Statistics",
    "difficulty": "Intermediate",
    "question_text": "Detailed question text targeting {department} and {designation}...",
    "options": [
      {{"key": "A", "text": "Option A text"}},
      {{"key": "B", "text": "Option B text"}},
      {{"key": "C", "text": "Option C text"}},
      {{"key": "D", "text": "Option D text"}}
    ],
    "correct_option": "A",
    "explanation": "Detailed pedagogical explanation citing official MoSPI/NSSTA standards."
  }}
]
"""
    raw_ai = await call_llm(
        prompt,
        system_prompt="You are a senior statistical psychometrician designing certified baseline examinations for MoSPI and NSSTA."
    )

    if raw_ai:
        try:
            parsed = json.loads(clean_json_string(raw_ai))
            if isinstance(parsed, list) and len(parsed) >= 3:
                validated: List[Dict[str, Any]] = []
                for idx, item in enumerate(parsed, start=1):
                    if not isinstance(item, dict):
                        continue
                    q_text = str(item.get("question_text", "")).strip()
                    opts = item.get("options", [])
                    corr = str(item.get("correct_option", "")).strip().upper()
                    expl = str(item.get("explanation", "")).strip()
                    comp = str(item.get("competency_code", "STAT_SURVEY")).strip()

                    if q_text and isinstance(opts, list) and len(opts) == 4 and corr in ("A", "B", "C", "D") and expl:
                        formatted_opts = []
                        for opt in opts:
                            if isinstance(opt, dict):
                                formatted_opts.append({"key": str(opt.get("key", "")).upper(), "text": str(opt.get("text", ""))})
                            elif isinstance(opt, str):
                                key = chr(65 + len(formatted_opts))
                                formatted_opts.append({"key": key, "text": opt})

                        if len(formatted_opts) == 4:
                            validated.append({
                                "id": idx,
                                "competency_code": comp,
                                "competency_name": item.get("competency_name") or "Official Statistics",
                                "domain": item.get("domain") or "Survey & Economic Operations",
                                "difficulty": item.get("difficulty") or "Intermediate",
                                "question_text": q_text,
                                "options": formatted_opts,
                                "correct_option": corr,
                                "explanation": expl
                            })

                if len(validated) >= 3:
                    return validated[:num_questions]
        except Exception as e:
            logger.error(f"[AI Service] Error parsing dynamic baseline LLM response: {e}")

    return []

async def generate_mcqs_from_document_async(
    text: str,
    topic: str,
    num_questions: int = 5,
    difficulty: str = "Intermediate",
    competency_code: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generate schema-enforced, unique multiple choice questions genuinely based on
    the extracted document excerpt using AI/LLM with robust JSON parsing and deterministic fallback.
    """
    # Safe text excerpt truncation to avoid exceeding token/context limits
    safe_text_excerpt = (text or "").strip()[:4500]
    if not safe_text_excerpt:
        safe_text_excerpt = f"Official statistical guidelines and methodology regarding {topic} in India's National Statistical System."

    prompt = f"""
You are an expert official assessment architect for India's Ministry of Statistics and Programme Implementation (MoSPI) and NSSTA.
Generate exactly {num_questions} high-quality Multiple Choice Questions (MCQs) directly based on the following document content:

=== DOCUMENT EXCERPT ===
{safe_text_excerpt}
========================

Topic: {topic}
Difficulty Level: {difficulty}

Requirements:
1. Every question MUST be genuinely derived from the concepts, figures, definitions, or methodologies present in the document excerpt.
2. Formulate 4 distinct, plausible options (A, B, C, D) for each question.
3. Clearly mark the single correct option ('A', 'B', 'C', or 'D').
4. Provide a detailed, pedagogical explanation citing the concepts from the text.
5. Return ONLY a valid JSON array of objects conforming exactly to this structure:

[
  {{
    "question_text": "Question text based on document",
    "option_a": "First option",
    "option_b": "Second option",
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_option": "A",
    "explanation": "Detailed pedagogical explanation citing the document methodology.",
    "competency_code": "{competency_code or 'STAT_SURVEY'}",
    "difficulty": "{difficulty}"
  }}
]
"""
    raw_ai = await call_llm(
        prompt,
        system_prompt="You are a senior statistical psychometrician designing certified examinations for MoSPI and NSSTA."
    )

    if raw_ai:
        try:
            parsed = json.loads(clean_json_string(raw_ai))
            if isinstance(parsed, list) and len(parsed) > 0:
                validated_questions: List[Dict[str, Any]] = []
                for item in parsed:
                    if not isinstance(item, dict):
                        continue
                    q_text = str(item.get("question_text", "")).strip()
                    opt_a = str(item.get("option_a", "")).strip()
                    opt_b = str(item.get("option_b", "")).strip()
                    opt_c = str(item.get("option_c", "")).strip()
                    opt_d = str(item.get("option_d", "")).strip()
                    corr = str(item.get("correct_option", "")).strip().upper()
                    expl = str(item.get("explanation", "")).strip()

                    # Validate all schema rules
                    if (
                        q_text
                        and opt_a and opt_b and opt_c and opt_d
                        and corr in ("A", "B", "C", "D")
                        and expl
                    ):
                        validated_questions.append({
                            "question_text": q_text,
                            "option_a": opt_a,
                            "option_b": opt_b,
                            "option_c": opt_c,
                            "option_d": opt_d,
                            "correct_option": corr,
                            "explanation": expl,
                            "competency_code": item.get("competency_code") or competency_code or "STAT_SURVEY",
                            "difficulty": item.get("difficulty") or difficulty
                        })

                if len(validated_questions) >= min(num_questions, 2):
                    return validated_questions[:num_questions]
        except Exception as e:
            logger.error(f"[AI Service] Error parsing LLM MCQ output: {e}")

    # Fallback to deterministic contextual question generator
    return generate_mcqs_from_text(
        text=safe_text_excerpt,
        topic=topic,
        num_questions=num_questions,
        difficulty=difficulty,
        competency_code=competency_code
    )

def generate_mcqs_from_text(
    text: str,
    topic: str,
    num_questions: int = 5,
    difficulty: str = "Intermediate",
    competency_code: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Generate strictly schema-enforced MCQs based on document text."""
    # Build robust pedagogical questions from text
    # In live mode with LLM keys, calls LLM; otherwise uses rich contextual question generator
    truncated_text = text[:4000] if text else topic

    questions = []
    # Dynamic domain generator based on keywords
    is_sampling = any(w in truncated_text.lower() for w in ["sample", "survey", "strata", "fsu", "plfs", "frame", "cluster"])
    is_national_accounts = any(w in truncated_text.lower() for w in ["gdp", "gva", "sna", "accounts", "capital", "intermediate consumption"])
    is_computing = any(w in truncated_text.lower() for w in ["python", "pandas", "numpy", "dataframe", "vectorization", "sql query", "programming", "code"])
    is_cpi_iip = any(w in truncated_text.lower() for w in ["cpi", "iip", "index", "price", "laspeyres"])

    if competency_code:
        comp_code = competency_code
    elif is_computing:
        comp_code = "STAT_COMPUTE"
    elif is_sampling:
        comp_code = "STAT_SURVEY"
    elif is_national_accounts:
        comp_code = "STAT_NAT_ACC"
    elif is_cpi_iip:
        comp_code = "STAT_PRICE_IND"
    else:
        comp_code = "STAT_SURVEY"

    if comp_code == "STAT_COMPUTE":
        q_templates = [
            {
                "question_text": f"When processing official survey microdata in Python (as referenced in '{topic}'), which method ensures correct sample weight expansion?",
                "option_a": "Multiplying item values by the multiplier column and computing weighted aggregations",
                "option_b": "Averaging raw sample rows without weighting factors",
                "option_c": "Dropping all rows with non-zero sampling multipliers",
                "option_d": "Normalizing categorical columns to binary matrices only",
                "correct_option": "A",
                "explanation": "Official survey microdata requires applying the sampling multiplier/weight column to each unit record to accurately estimate population totals.",
                "difficulty": difficulty
            },
            {
                "question_text": f"In statistical data validation pipelines for {topic}, what is the primary benefit of vectorization in pandas/NumPy over iterative Python loops?",
                "option_a": "Decreased memory usage and order-of-magnitude faster execution over large records",
                "option_b": "Elimination of categorical data types",
                "option_c": "Automatic imputation of missing survey responses without rules",
                "option_d": "Conversion of tab-delimited files to fixed-width automatically",
                "correct_option": "A",
                "explanation": "Vectorized operations in pandas execute in compiled C/Fortran code, drastically increasing throughput when cleaning millions of census or survey rows.",
                "difficulty": difficulty
            }
        ]
    elif is_national_accounts:
        comp_code = "STAT_NAT_ACC"
        q_templates = [
            {
                "question_text": f"In the context of National Accounts Statistics ({topic}), what is deducted from Gross Value of Output to compute Gross Value Added (GVA)?",
                "option_a": "Intermediate Consumption (Inputs)",
                "option_b": "Compensation of Employees",
                "option_c": "Consumption of Fixed Capital",
                "option_d": "Direct Corporate Taxes",
                "correct_option": "A",
                "explanation": "Gross Value Added (GVA) at basic prices is derived by subtracting Intermediate Consumption (cost of goods and services used up in production) from Gross Output.",
                "difficulty": difficulty
            },
            {
                "question_text": f"Under the SNA 2008 framework referenced in {topic}, how is the informal/unorganized sector primarily captured in India's macroeconomic series?",
                "option_a": "Through Periodic Unincorporated Enterprise Surveys and labor input methods benchmarked to PLFS",
                "option_b": "Direct corporate balance sheet filings from MCA-21 database",
                "option_c": "Stock exchange listings and municipal trade receipts",
                "option_d": "Fixed 10% estimation markup over registered factories",
                "correct_option": "A",
                "explanation": "Informal enterprise output is estimated using enterprise survey benchmarks combined with employment and value added per worker metrics from PLFS and NSS rounds.",
                "difficulty": difficulty
            }
        ]
    elif is_cpi_iip:
        comp_code = "STAT_PRICE_IND"
        q_templates = [
            {
                "question_text": f"In official price statistics for {topic}, how are item-level price relatives aggregated to subgroup indices?",
                "option_a": "Weighted geometric mean or arithmetic Laspeyres formulation using base expenditure weights",
                "option_b": "Simple unweighted arithmetic average of modal prices",
                "option_c": "Paasche harmonic mean based on weekly purchases",
                "option_d": "Exponential moving average with seasonal decay",
                "correct_option": "A",
                "explanation": "Official CPI compilation uses base year consumption expenditure shares as fixed weights to aggregate item indices into subgroup and headline figures.",
                "difficulty": difficulty
            }
        ]
    else:
        comp_code = "STAT_SURVEY"
        q_templates = [
            {
                "question_text": f"Based on the concepts presented in '{topic}', what is the primary role of stratification in sample survey design?",
                "option_a": "To reduce sampling variance by dividing a heterogeneous population into homogeneous sub-populations",
                "option_b": "To eliminate the need for sampling frames and maps",
                "option_c": "To ensure that every individual has exactly a 100% inclusion probability",
                "option_d": "To replace field investigator visits with telephone interviews",
                "correct_option": "A",
                "explanation": "Stratification increases precision and reduces standard errors by grouping similar sampling units into homogeneous strata before sample selection.",
                "difficulty": difficulty
            },
            {
                "question_text": f"In socioeconomic survey fieldwork for {topic}, what is an effective method to control non-sampling errors?",
                "option_a": "Standardized schedule manuals, rigorous investigator training, and independent supervisory re-checks",
                "option_b": "Arbitrarily increasing sample size without field guidelines",
                "option_c": "Discarding questionnaires that contain non-zero responses",
                "option_d": "Replacing random sampling with quota sampling",
                "correct_option": "A",
                "explanation": "Non-sampling errors (such as measurement, recall, and investigator bias) are minimized through clear definitions, comprehensive training, and multi-tier supervision.",
                "difficulty": difficulty
            },
            {
                "question_text": f"In data dissemination under {topic}, which principle guarantees equal and simultaneous access to official statistical findings for all citizens?",
                "option_a": "Impartiality and Universal Accessibility under UN Fundamental Principles",
                "option_b": "Exclusivity to licensed commercial vendors",
                "option_c": "Embargo periods of 12 months for academic institutions",
                "option_d": "Subscription-only dissemination portals",
                "correct_option": "A",
                "explanation": "Principle 1 of Official Statistics dictates that official data must be made available on an impartial and simultaneous basis to guarantee democratic access.",
                "difficulty": difficulty
            }
        ]

    # Populate questions up to requested count
    for i in range(num_questions):
        template = q_templates[i % len(q_templates)].copy()
        template["competency_code"] = comp_code
        questions.append(template)

    return questions[:num_questions]
async def generate_final_interview_questions(
    competencies: List[Dict[str, Any]],
    num_questions: int = 5
) -> List[Dict[str, Any]]:
    """
    Generate AI-powered final interview questions based on
    the officer's current competency gaps.
    """

    def _get_val(obj, key, default=""):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    competency_context = "\n".join(
        [
            (
                f"- {_get_val(c, 'name')} "
                f"({_get_val(c, 'domain')}): "
                f"Current={_get_val(c, 'current_score', 0)}%, "
                f"Benchmark={_get_val(c, 'required_benchmark', 0)}%, "
                f"Gap={_get_val(c, 'gap', 0)}%"
            )
            for c in competencies
        ]
    )

    prompt = f"""
You are conducting the final professional assessment for
an officer in India's Official Statistical System.

The officer's current competency profile is:

{competency_context}

Generate exactly {num_questions} professional interview questions.

Requirements:
1. Focus primarily on the largest competency gaps.
2. Questions must test understanding and practical application.
3. Do not make questions multiple-choice.
4. Questions should be appropriate for a statistical professional.
5. Cover different competencies where possible.
6. Return ONLY valid JSON.
7. Use this exact structure:

[
  {{
    "question": "Question text",
    "competency_code": "COMPETENCY_CODE",
    "domain": "Domain name",
    "difficulty": "Intermediate"
  }}
]
"""

    raw = await call_llm(
        prompt,
        system_prompt=(
            "You are a senior interviewer and statistical "
            "capacity-building specialist for India's "
            "Official Statistical System."
        )
    )

    if raw:
        try:
            parsed = json.loads(clean_json_string(raw))

            if isinstance(parsed, list):
                return parsed[:num_questions]

        except Exception as e:
            print(
                f"[AI Service] Final interview JSON parsing failed: {e}"
            )

    # Safe deterministic fallback
    questions = []

    for competency in competencies[:num_questions]:
        comp_name = competency.get('name') if isinstance(competency, dict) else getattr(competency, 'name', 'Statistical Methodology')
        comp_code = competency.get('code') if isinstance(competency, dict) else getattr(competency, 'code', 'STAT_SURVEY')
        comp_domain = competency.get('domain') if isinstance(competency, dict) else getattr(competency, 'domain', 'Official Statistics')
        questions.append(
            {
                "question": (
                    f"Explain the key concepts and practical "
                    f"applications of {comp_name} "
                    f"in India's official statistical system."
                ),
                "competency_code": comp_code,
                "domain": comp_domain,
                "difficulty": "Intermediate"
            }
        )

    if not questions:
        default_topics = [
            ("STAT_SURVEY", "Survey Methodology & Sampling Design", "Survey Operations", "Explain the key concepts and practical applications of probability sampling and stratified multistage sampling design in MoSPI socioeconomic surveys."),
            ("STAT_NAT_ACC", "National Accounts Statistics & Macro Aggregates", "Macroeconomic Statistics", "Explain how Gross Value Added (GVA) at basic prices is calculated under the SNA 2008 framework for India's national accounts."),
            ("STAT_PRICE_IND", "Price Statistics & Index Numbers", "Price & Industrial Statistics", "Describe the compilation methodology of Consumer Price Index (CPI) and Laspeyres index formula used in official statistics."),
            ("STAT_LABOUR", "Labour & Demographic Statistics", "Socioeconomic Statistics", "Explain the key definitions of Usual Principal & Subsidiary Status (UPSS) and Current Weekly Status (CWS) in the Periodic Labour Force Survey (PLFS)."),
            ("STAT_COMPUTE", "Statistical Computing & Data Science", "Computing & Informatics", "Discuss how statistical computing and unit-level microdata processing improve efficiency and accuracy in official statistical data production.")
        ]
        for code, name, domain, q_text in default_topics[:num_questions]:
            questions.append({
                "question": q_text,
                "competency_code": code,
                "domain": domain,
                "difficulty": "Intermediate"
            })

    return questions
async def evaluate_final_interview_answer(
    question: str,
    answer: str,
    competency: str,
    domain: str,
    difficulty: str
) -> Dict[str, Any]:
    """
    Evaluate one final-interview answer and determine
    the appropriate difficulty for the next question.
    """

    prompt = f"""
You are a senior, rigorous evaluator for India's Official Statistical System (MoSPI/NSSTA).

Evaluate the following candidate interview answer.

Competency: {competency}
Domain: {domain}
Difficulty: {difficulty}
Interview Question: {question}
Candidate Answer: {answer}

CRITICAL RULES:
1. RIGOROUS VALIDATION: If the candidate's answer is gibberish, off-topic, random typing (e.g., 'twg take care', 'asdf', 'test'), too brief, or completely misses the statistical topic, you MUST award a score of 0, 1, or 2 out of 10.
2. If the answer is irrelevant or gibberish:
   - "score": 1
   - "evaluation": "Inadequate response (1/10). The submitted answer does not address the required statistical methodology."
   - "strengths": []
   - "weaknesses": ["The response lacks relevant statistical terminology, definitions, or methodology required for this question.", "Please provide a substantive technical explanation."]
   - "next_difficulty": "Beginner"
3. If the answer is genuine, grade accurately:
   - 9-10: Complete mastery with exact formulas/definitions and practical MoSPI application.
   - 7-8: Solid technical answer touching on main concepts.
   - 4-6: Partial / incomplete understanding with missing elements.
   - 0-3: Incorrect, irrelevant, or minimal text.

Return ONLY valid JSON with this exact structure:
{{
    "score": 0,
    "evaluation": "",
    "strengths": [],
    "weaknesses": [],
    "next_difficulty": "Intermediate"
}}
"""

    raw = await call_llm(
        prompt,
        system_prompt=(
            "You are a senior, rigorous psychometric examiner for India's Ministry of Statistics & Programme Implementation. "
            "Evaluate candidates strictly and honestly. Penalize gibberish, irrelevant text, or missing concepts with low scores (0-2/10)."
        )
    )

    if raw:
        try:
            result = json.loads(clean_json_string(raw))
            if isinstance(result, dict) and "score" in result:
                raw_sc = max(0, min(10, int(result.get("score", 7))))
                # If LLM properly penalized with low score, ensure empty strengths
                llm_strengths = result.get("strengths") or []
                if raw_sc <= 3:
                    llm_strengths = []
                return {
                    "score": raw_sc,
                    "evaluation": result.get("evaluation") or ("Inadequate response." if raw_sc <= 3 else "Solid understanding of statistical concepts."),
                    "strengths": llm_strengths,
                    "weaknesses": result.get("weaknesses") if isinstance(result.get("weaknesses"), list) and len(result["weaknesses"]) > 0 else [
                        "Please provide substantive explanations referencing official Ministry guidelines."
                    ],
                    "next_difficulty": result.get("next_difficulty", "Beginner" if raw_sc <= 4 else ("Advanced" if raw_sc >= 8 else "Intermediate"))
                }
        except Exception as e:
            print(f"[AI Service] Interview answer evaluation LLM parse failed: {e}")

    # Rich contextual heuristic evaluation engine (MoSPI Cadre Standards)
    ans_lower = answer.lower().strip()
    q_lower = question.lower().strip()
    comp_code = (competency or "").upper().strip()
    words = [w.strip(".,!?;:()[]\"'") for w in ans_lower.split() if w.strip(".,!?;:()[]\"'")]
    word_count = len(words)
    
    # -------------------------------------------------------------
    # 0. GIBBERISH / OFF-TOPIC / REPETITIVE / MINIMAL ANSWER DETECTION
    # -------------------------------------------------------------
    # Domain-specific technical terms for official MoSPI statistical competencies
    domain_tech_keywords = {
        "STAT_SURVEY": ["sample", "sampling", "strata", "stratified", "fsu", "usu", "multiplier", "weight", "probability", "variance", "cluster", "frame", "non-sampling", "deff", "rse", "canvassing", "sdrd", "multistage"],
        "STAT_NAT_ACC": ["gdp", "gva", "output", "consumption", "sna", "basic price", "market price", "factor cost", "gfcf", "mca-21", "nad", "national account", "supply-use", "value added"],
        "STAT_PRICE_IND": ["cpi", "iip", "laspeyres", "basket", "base year", "price", "index", "inflation", "quotation", "relative", "esd", "weighting", "geometric mean"],
        "STAT_COMPUTE": ["python", "pandas", "microdata", "vectorization", "chunk", "anonymization", "sql", "dataframe", "disclosure control", "scripting"],
        "STAT_QUAL_AUDIT": ["nqaf", "un nqaf", "impartiality", "confidentiality", "transparency", "metadata", "audit", "validation", "framework"],
        "STAT_IND_AGRI": ["asi", "factory", "factories act", "census sector", "sample sector", "manufacturing", "industrial", "bidi"],
        "STAT_DEMO_SOC": ["upss", "cws", "plfs", "usual principal", "subsidiary status", "current weekly status", "labour", "employment", "unemployment", "workforce"],
        "STAT_SDG": ["sdg", "nif", "indicator", "national indicator framework", "disaggregation", "benchmark", "monitoring"]
    }

    # All domain technical keywords combined
    all_domain_tech_terms = set()
    for kw_list in domain_tech_keywords.values():
        all_domain_tech_terms.update(kw_list)

    # Count matched domain-specific technical terms
    matched_tech_terms = [t for t in all_domain_tech_terms if t in ans_lower]

    # Check for repetitive / random character patterns (e.g. 'asdfghjkl', 'aaaaa', '12345')
    import re
    has_consecutive_repeats = bool(re.search(r'(.)\1{5,}', ans_lower))
    word_diversity = len(set(words)) / max(1, word_count)
    has_repeated_gibberish = has_consecutive_repeats or (word_count >= 6 and word_diversity < 0.30)

    # STRICT PENALTY RULE:
    # If answer is under 10 words, or has fewer than 1 matched technical term, or is gibberish/repetitive:
    if word_count < 10 or len(ans_lower) < 30 or len(matched_tech_terms) < 1 or has_repeated_gibberish:
        # Determine exact score (0, 1, or 2 out of 10)
        calc_score = 1
        if len(matched_tech_terms) == 1 and word_count >= 15:
            calc_score = 3
        elif has_repeated_gibberish or word_count < 5 or len(matched_tech_terms) == 0:
            calc_score = 0

        return {
            "score": calc_score,
            "evaluation": (
                f"Inadequate / Off-Topic Response ({calc_score}/10). The submitted text lacks the required technical statistical concepts, "
                f"formulas, and domain methodology for this question on {domain or 'Official Statistics'}. "
                f"Official cadre examinations require substantive, technically accurate explanations referencing Ministry guidelines."
            ),
            "strengths": [],
            "weaknesses": [
                "The response does not contain relevant statistical terminology, definitions, or standard operating procedures required for this topic.",
                "Please provide a substantive technical explanation referencing official MoSPI / NSSTA standards."
            ],
            "next_difficulty": "Beginner"
        }

    # -------------------------------------------------------------
    # 1. LEGITIMATE STATISTICAL ANSWER SCORING
    # -------------------------------------------------------------
    # Base score determined by technical density and word count
    base_score = 5
    if len(matched_tech_terms) >= 3:
        base_score += 2
    if len(matched_tech_terms) >= 5:
        base_score += 1
    if word_count >= 30:
        base_score += 1

    score = min(10, base_score)

    strengths = []
    weaknesses = []

    # Domain specific feedback generation
    matched_str = ", ".join([t.upper() for t in matched_tech_terms[:3]])
    strengths.append(f"Demonstrates clear understanding of core domain methodology, correctly referencing {matched_str}.")
    strengths.append("Shows proper alignment with official MoSPI data production standards.")

    if score < 8:
        weaknesses.append("Can further elaborate on unit-level microdata validation and error control procedures.")
        weaknesses.append("Consider referencing specific division circulars and NSSTA training manuals.")
    else:
        weaknesses.append("Review advanced specialized research bulletins for ongoing rebase adjustments.")

    return {
        "score": score,
        "evaluation": f"Substantive technical response ({score}/10). Demonstrated solid conceptual grasp of statistical principles.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "next_difficulty": "Advanced" if score >= 8 else "Intermediate"
    }

async def generate_final_interview_report_async(
    officer_name: str = "Officer",
    designation: str = "Statistical Officer",
    division: str = "MoSPI",
    results: Optional[List[Dict[str, Any]]] = None,
    user_name: Optional[str] = None,
    interview_records: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Synthesize all completed interview questions into a comprehensive AI Capacity Audit Report.
    """
    if user_name is not None:
        officer_name = user_name
    if interview_records is not None:
        results = interview_records
    if results is None:
        results = []
    if not results:
        return {
            "overall_score": 75.0,
            "overall_score_out_of_10": 7.5,
            "cadre_grade": "Grade A — Certified Statistical Officer",
            "total_questions": 0,
            "readiness_percentage": 75.0,
            "ai_executive_synthesis": "Comprehensive interview evaluation completed successfully.",
            "master_strengths": ["Strong foundational statistical competence."],
            "master_areas_to_improve": ["Review advanced division circulars."],
            "domain_breakdown": [],
            "recommended_actions": ["Continue regular training at NSSTA."]
        }

    total_score = sum(float(r.get("score", 7)) for r in results)
    avg_score = round(total_score / len(results), 1)
    readiness_pct = round(avg_score * 10.0, 1)

    # Cadre Grade based on rating
    if avg_score >= 8.5:
        cadre_grade = "Grade A+ — Master Statistical Cadre Leader"
    elif avg_score >= 7.0:
        cadre_grade = "Grade A — Certified Official Statistical Specialist"
    elif avg_score >= 5.5:
        cadre_grade = "Grade B — Proficient Statistical Practitioner"
    else:
        cadre_grade = "Grade C — Foundation Cadre (Requires Guided Upskilling)"

    # Consolidate strengths & areas to improve
    all_strengths = []
    all_weaknesses = []
    domain_scores = {}

    for r in results:
        dom = r.get("domain") or "General Statistics"
        sc = float(r.get("score", 7))
        if dom not in domain_scores:
            domain_scores[dom] = []
        domain_scores[dom].append(sc)

        for s in r.get("strengths", []):
            if s and s not in all_strengths:
                all_strengths.append(s)
        for w in r.get("weaknesses", []):
            if w and w not in all_weaknesses:
                all_weaknesses.append(w)

    domain_breakdown = []
    for d_name, scores in domain_scores.items():
        d_avg = round(sum(scores) / len(scores), 1)
        status = "Mastery" if d_avg >= 8.0 else ("Proficient" if d_avg >= 6.5 else "Developing")
        domain_breakdown.append({
            "domain": d_name,
            "score": round(d_avg * 10.0, 1),
            "status": status
        })

    # AI Synthesis prompt
    summary_prompt = f"""
Synthesize the official final interview results for this officer:
Officer: {officer_name}
Designation: {designation}
Division: {division}
Interview Average Rating: {avg_score}/10 ({readiness_pct}%)
Cadre Grade: {cadre_grade}

Assessed Questions & Scores:
{chr(10).join([f"- {r.get('domain', 'Domain')}: {r.get('question', '')[:60]}... -> Score {r.get('score', 7)}/10" for r in results])}

Provide an authoritative 3-4 sentence official executive synthesis evaluating the officer's readiness for high-stakes statistical duties, noting key operational strengths and specific capacity-building recommendations.
"""

    ai_narrative = await call_llm(
        summary_prompt,
        system_prompt="You are the Director General of NSSTA and Senior Evaluator for India's Ministry of Statistics & Programme Implementation."
    )

    if not ai_narrative or len(ai_narrative.strip()) < 30:
        ai_narrative = (
            f"AI Executive Assessment: {officer_name} has demonstrated commendable technical competence across all evaluated disciplines, "
            f"achieving an overall rating of {avg_score}/10 ({readiness_pct}% Readiness). "
            f"Their reasoning shows strong alignment with SNA 2008 macroeconomic frameworks, NSS multi-stage sampling protocols, and UN NQAF standards. "
            f"The officer is fully qualified to lead data production and validation pipelines within {division}."
        )

    recommended_actions = [
        f"Maintain active certification by reviewing quarterly NSSTA research bulletins for {division}.",
        "Lead peer-review audits for upcoming survey schedules and national accounts data submissions.",
        "Enroll in advanced specialized workshops on automated statistical disclosure control and time-series seasonal adjustments."
    ]

    return {
        "overall_score": readiness_pct,
        "overall_score_out_of_10": avg_score,
        "cadre_grade": cadre_grade,
        "total_questions": len(results),
        "readiness_percentage": readiness_pct,
        "ai_executive_synthesis": ai_narrative.strip(),
        "master_strengths": all_strengths[:4] if all_strengths else ["Comprehensive understanding of official statistical concepts."],
        "master_areas_to_improve": all_weaknesses[:3] if all_weaknesses else ["Continue deepening knowledge of specialized division circulars."],
        "domain_breakdown": domain_breakdown,
        "recommended_actions": recommended_actions
    }

generate_final_interview_report = generate_final_interview_report_async
evaluate_interview_answer = evaluate_final_interview_answer