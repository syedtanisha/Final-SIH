from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    designation = Column(String(255), default="Statistical Professional")
    department = Column(String(255), default="MoSPI")
    organization = Column(String(255), default="Government of India")
    role = Column(String(50), default="user")  # 'user', 'trainer', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    competencies = relationship("UserCompetency", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", foreign_keys="Document.user_id", back_populates="user", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("LearningProgressHistory", back_populates="user", cascade="all, delete-orphan")
    baseline_assignments = relationship("BaselineAssignment", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class BaselineAssignment(Base):
    __tablename__ = "baseline_assignments"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    designation = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    role_tier = Column(String(50), nullable=False)  # 'senior', 'mid', 'junior', 'technical'
    resolution_method = Column(String(50), default="exact")
    blueprint_version = Column(String(50), default="v1")
    assigned_question_ids = Column(Text, nullable=False)  # JSON string of question IDs list
    total_questions = Column(Integer, default=9)
    status = Column(String(50), default="assigned")  # 'assigned', 'submitted'
    score = Column(Float, nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="baseline_assignments")


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    domain = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    required_level = Column(Float, default=80.0)  # Benchmark target percentage
    weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_competencies = relationship("UserCompetency", back_populates="competency")
    resource_mappings = relationship("ResourceCompetencyMapping", back_populates="competency")


class UserCompetency(Base):
    __tablename__ = "user_competencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False, index=True)
    current_level = Column(Float, default=0.0)  # percentage: 0.0 to 100.0
    last_assessed_at = Column(DateTime, default=datetime.utcnow)
    assessment_source = Column(String(50), default="initial")

    user = relationship("User", back_populates="competencies")
    competency = relationship("Competency", back_populates="user_competencies")

    __table_args__ = (UniqueConstraint('user_id', 'competency_id', name='_user_competency_uc'),)


class OfficialSource(Base):
    __tablename__ = "official_sources"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    organization = Column(String(100), nullable=False)  # 'NSSTA', 'MoSPI', 'eSankhyiki'
    base_url = Column(String(1000), nullable=False)
    source_type = Column(String(100), nullable=False)  # 'Official Public Data', 'Official Metadata', 'Official Training Resource', 'Restricted Data', 'Curated Metadata'
    access_method = Column(String(100), nullable=False)  # 'Official API', 'Downloadable CSV', 'Downloadable Excel', 'Downloadable JSON', 'Dataset Catalogue', 'Publication', 'Training Resource', 'Microdata Metadata', 'Restricted/Authenticated Data'
    authentication_required = Column(Boolean, default=False)
    access_level = Column(String(50), default="PUBLIC")  # 'PUBLIC', 'REGISTERED', 'RESTRICTED', 'METADATA_ONLY'
    enabled = Column(Boolean, default=True)
    last_checked_at = Column(DateTime, default=datetime.utcnow)

    resources = relationship("LearningResource", back_populates="official_source")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String(50), nullable=False)  # 'NSSTA', 'MoSPI', 'eSankhyiki'
    official_url = Column(String(1000), nullable=False)
    resource_type = Column(String(50), nullable=False)  # 'CBP_Course', 'Training_Module', 'Publication', 'Dataset', 'Video'
    difficulty = Column(String(50), default="Intermediate")
    estimated_duration_mins = Column(Integer, default=60)
    publisher_org = Column(String(100), nullable=True)
    provenance_type = Column(String(100), default="Curated Official Metadata")
    reference_period = Column(String(100), nullable=True)
    thumbnail_url = Column(String(1000), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Official Integration Layer Extensions
    source_id = Column(Integer, ForeignKey("official_sources.id", ondelete="SET NULL"), nullable=True)
    source_format = Column(String(50), nullable=True)  # 'CSV', 'Excel', 'JSON', 'PDF', 'API', 'HTML', 'Catalogue'
    access_level = Column(String(50), default="PUBLIC")  # 'PUBLIC', 'REGISTERED', 'RESTRICTED', 'METADATA_ONLY'
    publication_date = Column(String(100), nullable=True)
    version = Column(String(50), nullable=True)
    dedup_hash = Column(String(255), unique=True, index=True, nullable=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    role_relevance = Column(String(255), nullable=True)
    provider_external_id = Column(String(100), nullable=True)
    verification_level = Column(String(50), default="PORTAL_VERIFIED")  # 'PORTAL_VERIFIED', 'PAGE_VERIFIED', 'RESOURCE_VERIFIED', 'UNVERIFIED'

    official_source = relationship("OfficialSource", back_populates="resources")
    competency_mappings = relationship("ResourceCompetencyMapping", back_populates="resource", cascade="all, delete-orphan")


class ResourceCompetencyMapping(Base):
    __tablename__ = "resource_competency_mappings"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("learning_resources.id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False)
    relevance_score = Column(Float, default=1.0)
    mapping_provenance = Column(String(100), default="Platform Curated Competency Mapping")

    resource = relationship("LearningResource", back_populates="competency_mappings")
    competency = relationship("Competency", back_populates="resource_mappings")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    extracted_text = Column(Text, nullable=False)
    character_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Phase 4 Extensions
    content_hash = Column(String(64), index=True, nullable=True)
    extraction_status = Column(String(50), default="SUCCESS")  # 'SUCCESS', 'FAILED', 'PARTIAL'
    processing_status = Column(String(50), default="PROCESSED")  # 'PENDING', 'PROCESSED', 'CHUNKED', 'MAPPED'
    suggested_competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    mapping_confidence = Column(Float, default=0.85)
    mapping_method = Column(String(100), default="PLATFORM_HEURISTIC")  # 'EXPLICIT_DECLARED', 'PLATFORM_HEURISTIC', 'SEMANTIC_AI'
    mapping_overridden_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    overridden_at = Column(DateTime, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="documents")
    quizzes = relationship("Quiz", back_populates="document")
    chunks = relationship("ContentChunk", back_populates="document", cascade="all, delete-orphan")
    suggested_competency = relationship("Competency", foreign_keys=[suggested_competency_id])
    overrider = relationship("User", foreign_keys=[mapping_overridden_by])


class ContentChunk(Base):
    __tablename__ = "content_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    character_count = Column(Integer, default=0)
    token_count_approx = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="chunks")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    total_questions = Column(Integer, default=5)
    time_limit_mins = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Phase 4 Extensions
    purpose = Column(String(50), default="SELF_ASSESSMENT")  # 'PRACTICE', 'SELF_ASSESSMENT', 'TRAINER_ASSESSMENT', 'POST_TRAINING'
    blueprint_metadata = Column(Text, nullable=True)  # JSON representation of assessment blueprint
    generation_method = Column(String(100), default="DETERMINISTIC_FALLBACK")  # 'LIVE_LLM', 'LOCAL_AI', 'DETERMINISTIC_FALLBACK'

    user = relationship("User", back_populates="quizzes")
    document = relationship("Document", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = Column(Text, nullable=False)
    competency_code = Column(String(50), nullable=True)
    difficulty = Column(String(50), default="Intermediate")

    # Phase 4 Extensions
    source_reference = Column(String(255), nullable=True)  # e.g. "doc:1#chunk:0"
    generation_method = Column(String(100), default="DETERMINISTIC_FALLBACK")
    competency_mapping_method = Column(String(100), default="PLATFORM_HEURISTIC")

    quiz = relationship("Quiz", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    total_correct = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    competency_score_before = Column(Float, default=0.0)
    competency_score_after = Column(Float, default=0.0)
    competency_delta = Column(Float, default=0.0)
    ai_qualitative_feedback = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

    # Phase 4 Extensions
    status = Column(String(50), default="EVALUATED")  # 'ASSIGNED', 'IN_PROGRESS', 'SUBMITTED', 'EVALUATED'
    feedback_method = Column(String(100), default="Deterministic Pedagogical Feedback")  # 'Deterministic Pedagogical Feedback', 'AI-Generated Feedback'
    evidence_key = Column(String(255), unique=True, index=True, nullable=True)

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")


class UserResourceProgress(Base):
    __tablename__ = "user_resource_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resource_id = Column(Integer, ForeignKey("learning_resources.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="NOT_STARTED")  # 'NOT_STARTED', 'IN_PROGRESS', 'COMPLETED'
    progress_percentage = Column(Float, default=0.0)
    time_spent_mins = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)
    evidence_processed = Column(Boolean, default=False)
    evidence_key = Column(String(255), unique=True, index=True, nullable=True)

    user = relationship("User")
    resource = relationship("LearningResource")

    __table_args__ = (UniqueConstraint('user_id', 'resource_id', name='_user_resource_progress_uc'),)


class LearningProgressHistory(Base):
    __tablename__ = "learning_progress_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    previous_score = Column(Float, nullable=False)
    new_score = Column(Float, nullable=False)
    delta = Column(Float, nullable=False)
    evidence_key = Column(String(255), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_records")
    competency = relationship("Competency")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, default="Capacity Building Assistant Session")
    status = Column(String(50), default="active")  # 'active', 'deleted', 'archived'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("chat_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # 'USER', 'ASSISTANT', 'SYSTEM'
    content = Column(Text, nullable=False)
    response_method = Column(String(100), nullable=True)  # 'LIVE_LLM', 'DETERMINISTIC_FALLBACK'
    model_provider = Column(String(100), nullable=True)
    retrieval_used = Column(Boolean, default=False)
    retrieved_chunk_ids = Column(Text, nullable=True)  # JSON string of source references
    competency_context_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
    user = relationship("User")
