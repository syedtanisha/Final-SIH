from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class EvidenceLevelEnum(str, Enum):
    HIGH_EVIDENCE = "HIGH_EVIDENCE"
    MODERATE_EVIDENCE = "MODERATE_EVIDENCE"
    LIMITED_EVIDENCE = "LIMITED_EVIDENCE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

class DataStatusEnum(str, Enum):
    VALID = "VALID"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NO_EVIDENCE = "NO_EVIDENCE"

class EmergingSignalEnum(str, Enum):
    EMERGING = "EMERGING"
    GROWING = "GROWING"
    STABLE = "STABLE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

# 1. Workforce Overview
class WorkforceOverviewOut(BaseModel):
    total_officers: int
    active_users: int
    total_competencies_tracked: int
    organization_readiness_score: float = Field(..., description="Mean readiness score across all officers (0.0 to 100.0)")
    high_priority_gap_count: int
    officers_meeting_benchmarks_pct: float
    evidence_level: EvidenceLevelEnum
    calculation_method: str
    sample_size: int

# 2. Competency Analytics
class CompetencyDistributionItem(BaseModel):
    code: str
    name: str
    domain: str
    required_level: float
    average_current_level: float
    average_gap: float
    affected_officers_count: int
    meeting_benchmark_pct: float
    priority_rank: int

class CompetencyAnalyticsOut(BaseModel):
    competencies: List[CompetencyDistributionItem]
    highest_gap_competency: str
    sample_size: int
    evidence_level: EvidenceLevelEnum
    calculation_method: str

# 3. Department & Role Tier Analytics
class DepartmentBreakdownItem(BaseModel):
    department: str
    officer_count: int
    average_readiness_score: float
    primary_focus_gap: str
    meeting_benchmark_pct: float

class RoleTierBreakdownItem(BaseModel):
    role_tier: str
    officer_count: int
    average_readiness_score: float
    primary_focus_gap: str

class DepartmentAnalyticsOut(BaseModel):
    departments: List[DepartmentBreakdownItem]
    role_tiers: List[RoleTierBreakdownItem]
    sample_size: int
    evidence_level: EvidenceLevelEnum
    calculation_method: str

# 4. Training Effectiveness Analytics
class CompetencyGainSummaryItem(BaseModel):
    code: str
    name: str
    total_events: int
    avg_gain_delta: float
    max_gain_delta: float

class ProgressionSummaryItem(BaseModel):
    competency_code: str
    avg_before_score: float
    avg_after_score: float
    avg_delta: float

class TrainingEffectivenessOut(BaseModel):
    data_status: DataStatusEnum
    resources_started: int
    resources_completed: int
    completion_rate_pct: float
    total_quiz_attempts: int
    average_quiz_score: float
    average_competency_gain: float
    learning_gains_by_competency: List[CompetencyGainSummaryItem]
    before_after_progression: List[ProgressionSummaryItem]
    sample_size: int
    evidence_level: EvidenceLevelEnum
    calculation_method: str

# 5. Workforce Skill-Gap Intelligence
class CriticalGapSummaryItem(BaseModel):
    code: str
    name: str
    domain: str
    avg_gap: float
    affected_officer_count: int
    priority_score: float
    formula_explanation: str

class SkillGapIntelligenceOut(BaseModel):
    top_critical_gaps: List[CriticalGapSummaryItem]
    gaps_by_department: Dict[str, List[str]]
    gaps_by_role_tier: Dict[str, List[str]]
    highest_training_priority_competency: str
    priority_formula: str
    sample_size: int
    evidence_level: EvidenceLevelEnum

# 6. Emerging Skill Requirement Detection
class EmergingSkillSignalItem(BaseModel):
    competency_code: str
    competency_name: str
    signal_status: EmergingSignalEnum
    affected_officers_pct: float
    recommendation_frequency: int
    growth_trend: str
    evidence_rationale: str

class EmergingSkillIntelligenceOut(BaseModel):
    signals: List[EmergingSkillSignalItem]
    overall_signal_summary: str
    sample_size: int
    evidence_level: EvidenceLevelEnum
    calculation_method: str

# 7. Capacity-Building Forecast
class CapacityForecastOut(BaseModel):
    forecast_status: DataStatusEnum
    forecast_method: str = "Empirical Historical Gain Rate Extrapolation Model"
    top_priority_training_competencies: List[str]
    total_officers_needing_capacity_building: int
    current_organizational_readiness: float
    projected_readiness_improvement: float
    projected_readiness_60d: float
    projected_readiness_90d: float
    historical_gain_rate_per_activity: float
    assumptions: List[str]
    evidence_level: EvidenceLevelEnum
    calculation_method: str
