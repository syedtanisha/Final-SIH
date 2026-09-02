from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CompetencyBase(BaseModel):
    code: str
    name: str
    domain: str
    description: Optional[str] = None
    required_level: float = 80.0
    weight: float = 1.0

class CompetencyCreate(CompetencyBase):
    pass

class CompetencyOut(CompetencyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCompetencyDetail(BaseModel):
    competency_id: int
    code: str
    name: str
    domain: str
    description: Optional[str] = None
    required_level: float
    current_level: float
    gap: float
    priority: str  # 'High', 'Medium', 'Low', 'Met'
    is_role_core: bool = False
    last_assessed_at: Optional[datetime] = None

class CompetencyProfileOut(BaseModel):
    overall_readiness_score: float
    total_competencies: int
    competencies_met_count: int
    active_gaps_count: int
    user_division: Optional[str] = None
    user_designation: Optional[str] = None
    cadre_seniority: Optional[str] = None
    competencies: List[UserCompetencyDetail]

class CompetencyGapItem(BaseModel):
    competency_id: int
    code: str
    name: str
    domain: str
    current_level: float
    required_level: float
    gap: float
    priority: str
    priority_score: float
    is_role_core: bool = False
    recommended_focus_action: str

class CompetencyGapAnalysisOut(BaseModel):
    total_gaps_identified: int
    critical_gaps_count: int
    primary_focus_domain: str
    user_division: Optional[str] = None
    user_designation: Optional[str] = None
    cadre_seniority: Optional[str] = None
    gaps: List[CompetencyGapItem]
    ai_diagnosis_summary: str

# Resource and Recommendation Schemas
class LearningResourceOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    source: str  # 'NSSTA', 'MoSPI', 'eSankhyiki'
    official_url: str
    resource_type: str
    difficulty: str
    estimated_duration_mins: int
    publisher_org: Optional[str] = None
    provenance_type: Optional[str] = None
    reference_period: Optional[str] = None
    access_level: Optional[str] = "PUBLIC"
    source_format: Optional[str] = None
    publication_date: Optional[str] = None
    version: Optional[str] = None
    thumbnail_url: Optional[str] = None
    aligned_competencies: List[str] = []
    provider_external_id: Optional[str] = None
    verification_level: Optional[str] = "PORTAL_VERIFIED"
    mapping_provenance: Optional[str] = "Platform Curated Competency Mapping"

    class Config:
        from_attributes = True

class RecommendationItem(BaseModel):
    resource: LearningResourceOut
    matched_competency_code: str
    matched_competency_name: str
    competency_gap: float
    relevance_reason: str
    match_score: float

class RecommendationResponse(BaseModel):
    primary_focus_gap: str
    gap_percentage: float
    total_recommendations: int
    recommendations: List[RecommendationItem]
    ai_curation_note: str

class LearningPathMilestone(BaseModel):
    phase_number: int
    title: str
    domain: str
    description: str
    recommended_resource: str
    resource_id: Optional[int] = None
    official_url: Optional[str] = None
    estimated_hours: float
    action_type: str  # 'assessment', 'course', 'lab', 'quiz', 'interview'
    action_link: str
    completed: bool = False
    competency_code: Optional[str] = None

class LearningPathResponse(BaseModel):
    user_id: int
    officer_name: str
    designation: str
    division: str
    overall_readiness_score: float
    primary_focus_gap: str
    total_milestones: int
    completed_milestones: int
    progress_percentage: int
    milestones: List[LearningPathMilestone]
    ai_curation_note: str

class OfficialSourceOut(BaseModel):
    id: int
    source_id: str
    name: str
    organization: str
    base_url: str
    source_type: str
    access_method: str
    authentication_required: bool
    access_level: str
    enabled: bool
    last_checked_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RefreshSourcesRequest(BaseModel):
    source_ids: Optional[List[str]] = None

class RefreshSourcesResponse(BaseModel):
    status: str
    message: str
    total_sources_processed: int
    items_discovered: int
    items_ingested: int
    items_updated: int
    duplicates_skipped: int
    errors: List[str]

class ResourceProgressOut(BaseModel):
    id: int
    user_id: int
    resource_id: int
    status: str
    progress_percentage: float
    time_spent_mins: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    last_accessed_at: datetime

    class Config:
        from_attributes = True

class ResourceProgressUpdateReq(BaseModel):
    progress_percentage: float
    time_spent_mins: Optional[int] = 0

class AdaptiveLearningPathStateOut(BaseModel):
    user_id: int
    officer_name: str
    designation: str
    division: str
    overall_readiness_score: float
    primary_focus_gap: str
    resources_in_progress: List[LearningResourceOut]
    resources_completed: List[LearningResourceOut]
    remaining_gaps: List[CompetencyGapItem]
    recent_learning_history: List[ProgressEventOut]
    learning_path_milestones: List[LearningPathMilestone]

