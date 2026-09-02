from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

# Baseline Assessment Schemas
class BaselineQuestionOption(BaseModel):
    key: str  # 'A', 'B', 'C', 'D'
    text: str

class BaselineQuestion(BaseModel):
    id: int
    competency_code: str
    competency_name: str
    domain: str
    question_text: str
    options: List[BaselineQuestionOption]
    difficulty: str
    is_common: bool = True
    category: str = "common"
    applicable_roles: Optional[List[str]] = None

class BaselineAssessmentOut(BaseModel):
    assessment_id: str
    title: str
    instructions: str
    total_questions: int
    time_limit_mins: int
    questions: List[BaselineQuestion]
    officer_designation: Optional[str] = None
    role_tier: Optional[str] = None
    common_core_count: Optional[int] = 5
    role_specific_count: Optional[int] = 4
    assessed_competencies: Optional[List[str]] = None

class BaselineAnswerSubmit(BaseModel):
    question_id: int
    selected_option: str  # 'A', 'B', 'C', 'D'

class BaselineAssessmentSubmit(BaseModel):
    answers: List[BaselineAnswerSubmit]

class BaselineAssessmentResultOut(BaseModel):
    overall_score: float
    total_correct: int
    total_questions: int
    domain_scores: Dict[str, float]
    competency_scores: Dict[str, float]
    initialized_competencies_count: int
    feedback_summary: str

# Quiz Schemas
class MCQOption(BaseModel):
    key: str
    text: str

class MCQGeneratedQuestion(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str = Field(..., description="Must be 'A', 'B', 'C', or 'D'")
    explanation: str
    difficulty: str = "Intermediate"
    competency_code: Optional[str] = None

class QuizGenerateRequest(BaseModel):
    document_id: Optional[int] = None
    resource_id: Optional[int] = None
    custom_text: Optional[str] = Field(None, max_length=50000)
    topic: str = Field(..., min_length=2, max_length=500)
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="Intermediate", pattern="^(Foundational|Beginner|Intermediate|Advanced|Expert)$")
    competency_id: Optional[int] = None

class QuizQuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str
    source_reference: Optional[str] = None
    generation_method: Optional[str] = "DETERMINISTIC_FALLBACK"
    competency_mapping_method: Optional[str] = "PLATFORM_HEURISTIC"

    class Config:
        from_attributes = True

class QuizQuestionDetailOut(QuizQuestionOut):
    correct_option: str
    explanation: str

class QuizOut(BaseModel):
    id: int
    title: str
    topic: str
    difficulty: str
    total_questions: int
    time_limit_mins: int
    purpose: Optional[str] = "SELF_ASSESSMENT"
    generation_method: Optional[str] = "DETERMINISTIC_FALLBACK"
    blueprint_metadata: Optional[str] = None
    created_at: datetime
    questions: List[QuizQuestionOut]

    class Config:
        from_attributes = True

class QuizAnswerSubmit(BaseModel):
    question_id: int
    selected_option: str = Field(..., max_length=10)

class QuizSubmitRequest(BaseModel):
    answers: List[QuizAnswerSubmit] = Field(..., min_length=1)

class QuestionResultDetail(BaseModel):
    question_id: int
    question_text: str
    user_selected: str
    correct_option: str
    is_correct: bool
    explanation: str
    source_reference: Optional[str] = None

class QuizAttemptResultOut(BaseModel):
    attempt_id: int
    quiz_id: int
    quiz_title: str
    score: float
    total_correct: int
    total_questions: int
    status: Optional[str] = "EVALUATED"
    feedback_method: Optional[str] = "Deterministic Pedagogical Feedback"
    competency_name: Optional[str] = None
    competency_score_before: float
    competency_score_after: float
    competency_delta: float
    ai_qualitative_feedback: str
    question_results: List[QuestionResultDetail]
    completed_at: datetime

# Document Schemas
class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size_bytes: int
    character_count: int
    preview_text: str
    content_hash: Optional[str] = None
    extraction_status: Optional[str] = "SUCCESS"
    processing_status: Optional[str] = "PROCESSED"
    suggested_competency_id: Optional[int] = None
    mapping_method: Optional[str] = "PLATFORM_HEURISTIC"
    created_at: datetime
    message: str

class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size_bytes: int
    character_count: int
    content_hash: Optional[str] = None
    extraction_status: Optional[str] = "SUCCESS"
    processing_status: Optional[str] = "PROCESSED"
    suggested_competency_id: Optional[int] = None
    mapping_confidence: Optional[float] = 0.85
    mapping_method: Optional[str] = "PLATFORM_HEURISTIC"
    created_at: datetime

    class Config:
        from_attributes = True

class ContentStatusOut(BaseModel):
    document_id: int
    filename: str
    file_type: str
    content_hash: Optional[str] = None
    extraction_status: str
    processing_status: str
    character_count: int
    chunk_count: int
    suggested_competency_id: Optional[int] = None
    mapping_confidence: Optional[float] = 0.85
    mapping_method: str

class CompetencyMappingOverrideRequest(BaseModel):
    competency_id: int

class AssessmentBlueprintOut(BaseModel):
    total_questions: int
    mcq_count: int
    difficulty_distribution: Dict[str, int]
    competency_coverage: List[str]
    source_document_references: List[int]
    requested_difficulty: str
    purpose: str

# Progress Schemas
class ProgressEventOut(BaseModel):
    id: int
    competency_id: int
    competency_name: str
    domain: str
    event_type: str
    previous_score: float
    new_score: float
    delta: float
    created_at: datetime

    class Config:
        from_attributes = True

class CompetencyProgressCard(BaseModel):
    competency_id: int
    code: str
    name: str
    domain: str
    initial_score: float
    current_score: float
    required_benchmark: float
    total_gain: float
    status: str

class ProgressSummaryOut(BaseModel):
    user_id: int
    user_name: str
    designation: str
    department: str
    overall_readiness_score: float
    total_learning_gain: float
    quizzes_completed: int
    average_quiz_score: float
    competency_breakdown: List[CompetencyProgressCard]
    recent_events: List[ProgressEventOut]
    progress_events: List[ProgressEventOut] = []


# Final Interview Schemas
class FinalInterviewCompetency(BaseModel):
    competency_id: int
    code: str
    name: str
    domain: str
    current_score: float
    required_benchmark: float
    gap: float

class FinalInterviewReadiness(BaseModel):
    eligible: bool
    readiness_score: float
    competencies_to_assess: List[FinalInterviewCompetency]
    message: str

class FinalInterviewAnswerSubmit(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000)
    answer: str = Field(..., min_length=2, max_length=5000)
    competency: str = Field(..., min_length=2, max_length=255)
    domain: str = Field(..., min_length=2, max_length=255)
    difficulty: str = Field(default="Intermediate", pattern="^(Foundational|Beginner|Intermediate|Advanced|Expert)$")

class FinalInterviewAnswerEvaluation(BaseModel):
    score: int = Field(..., ge=0, le=10)
    evaluation: str
    strengths: List[str]
    weaknesses: List[str]
    next_difficulty: str

class InterviewQuestionRecord(BaseModel):
    question: str
    answer: str
    competency: Optional[str] = None
    domain: Optional[str] = None
    score: Optional[int] = 7
    evaluation: Optional[str] = None
    strengths: Optional[List[str]] = []
    weaknesses: Optional[List[str]] = []

class FinalInterviewReportRequest(BaseModel):
    results: List[InterviewQuestionRecord]

class DomainScoreBreakdown(BaseModel):
    domain: str
    score: float
    status: str

class FinalInterviewReportResponse(BaseModel):
    overall_score: float
    overall_score_out_of_10: float
    cadre_grade: str
    total_questions: int
    readiness_percentage: float
    ai_executive_synthesis: str
    master_strengths: List[str]
    master_areas_to_improve: List[str]
    domain_breakdown: List[DomainScoreBreakdown]
    recommended_actions: List[str]

