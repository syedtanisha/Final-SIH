from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .core.config import settings
from .db.database import engine, Base, SessionLocal
from .models.models import Competency, LearningResource, ResourceCompetencyMapping
from .data.seed_data import COMPETENCIES_SEED, RESOURCES_SEED
from .routers import auth, competencies, assessments, documents

def seed_initial_data():
    db: Session = SessionLocal()
    try:
        # 1. Seed Competencies if database is fresh
        if db.query(Competency).count() == 0:
            for c_data in COMPETENCIES_SEED:
                comp = Competency(
                    code=c_data["code"],
                    name=c_data["name"],
                    domain=c_data["domain"],
                    description=c_data["description"],
                    required_level=c_data["required_level"],
                    weight=c_data.get("weight", 1.0)
                )
                db.add(comp)
            db.commit()
            print("[INFO] Initialized 9 statistical competencies.")

        # 2. Seed Learning Resources and Mappings
        if db.query(LearningResource).count() == 0:
            all_comps = {c.code: c for c in db.query(Competency).all()}
            for r_data in RESOURCES_SEED:
                res = LearningResource(
                    title=r_data["title"],
                    description=r_data["description"],
                    source=r_data["source"],
                    official_url=r_data["official_url"],
                    resource_type=r_data["resource_type"],
                    difficulty=r_data["difficulty"],
                    estimated_duration_mins=r_data["estimated_duration_mins"],
                    publisher_org=r_data.get("publisher_org", r_data["source"]),
                    provenance_type=r_data.get("provenance_type", "Curated Official Metadata"),
                    reference_period=r_data.get("reference_period")
                )
                db.add(res)
                db.flush()

                comp_code = r_data.get("competency_code")
                if comp_code and comp_code in all_comps:
                    mapping = ResourceCompetencyMapping(
                        resource_id=res.id,
                        competency_id=all_comps[comp_code].id,
                        relevance_score=1.0
                    )
                    db.add(mapping)
            db.commit()
            print("[INFO] Seeded official iGOT, NSSTA, and MoSPI capacity building resources.")
    except Exception as e:
        db.rollback()
        print(f"[WARNING] Exception during initial data seed: {e}")
    finally:
        db.close()


def ensure_db_schema_migrated():
    from sqlalchemy import inspect, text
    inspector = inspect(engine)
    with engine.connect() as conn:
        if inspector.has_table("learning_resources"):
            cols = [c["name"] for c in inspector.get_columns("learning_resources")]
            if "publisher_org" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN publisher_org VARCHAR(100)"))
            if "provenance_type" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN provenance_type VARCHAR(100) DEFAULT 'Curated Official Metadata'"))
            if "reference_period" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN reference_period VARCHAR(100)"))
            if "source_id" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN source_id INTEGER"))
            if "source_format" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN source_format VARCHAR(50)"))
            if "access_level" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN access_level VARCHAR(50) DEFAULT 'PUBLIC'"))
            if "publication_date" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN publication_date VARCHAR(100)"))
            if "version" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN version VARCHAR(50)"))
            if "dedup_hash" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN dedup_hash VARCHAR(255)"))
            if "last_verified_at" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN last_verified_at DATETIME"))
            if "role_relevance" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN role_relevance VARCHAR(255)"))
            if "provider_external_id" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN provider_external_id VARCHAR(100)"))
            if "verification_level" not in cols:
                conn.execute(text("ALTER TABLE learning_resources ADD COLUMN verification_level VARCHAR(50) DEFAULT 'PORTAL_VERIFIED'"))
        if inspector.has_table("learning_progress_history"):
            cols = [c["name"] for c in inspector.get_columns("learning_progress_history")]
            if "evidence_key" not in cols:
                conn.execute(text("ALTER TABLE learning_progress_history ADD COLUMN evidence_key VARCHAR(255)"))
        if inspector.has_table("resource_competency_mappings"):
            cols = [c["name"] for c in inspector.get_columns("resource_competency_mappings")]
            if "mapping_provenance" not in cols:
                conn.execute(text("ALTER TABLE resource_competency_mappings ADD COLUMN mapping_provenance VARCHAR(100) DEFAULT 'Official FRAC Alignment'"))

        if inspector.has_table("documents"):
            cols = [c["name"] for c in inspector.get_columns("documents")]
            if "content_hash" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN content_hash VARCHAR(64)"))
            if "extraction_status" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN extraction_status VARCHAR(50) DEFAULT 'SUCCESS'"))
            if "processing_status" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN processing_status VARCHAR(50) DEFAULT 'PROCESSED'"))
            if "suggested_competency_id" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN suggested_competency_id INTEGER"))
            if "mapping_confidence" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN mapping_confidence FLOAT DEFAULT 0.85"))
            if "mapping_method" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN mapping_method VARCHAR(100) DEFAULT 'PLATFORM_HEURISTIC'"))
            if "mapping_overridden_by" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN mapping_overridden_by INTEGER"))
            if "overridden_at" not in cols:
                conn.execute(text("ALTER TABLE documents ADD COLUMN overridden_at DATETIME"))
        if inspector.has_table("quizzes"):
            cols = [c["name"] for c in inspector.get_columns("quizzes")]
            if "purpose" not in cols:
                conn.execute(text("ALTER TABLE quizzes ADD COLUMN purpose VARCHAR(50) DEFAULT 'SELF_ASSESSMENT'"))
            if "blueprint_metadata" not in cols:
                conn.execute(text("ALTER TABLE quizzes ADD COLUMN blueprint_metadata TEXT"))
            if "generation_method" not in cols:
                conn.execute(text("ALTER TABLE quizzes ADD COLUMN generation_method VARCHAR(100) DEFAULT 'DETERMINISTIC_FALLBACK'"))
        if inspector.has_table("quiz_questions"):
            cols = [c["name"] for c in inspector.get_columns("quiz_questions")]
            if "source_reference" not in cols:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN source_reference VARCHAR(255)"))
            if "generation_method" not in cols:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN generation_method VARCHAR(100) DEFAULT 'DETERMINISTIC_FALLBACK'"))
            if "competency_mapping_method" not in cols:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN competency_mapping_method VARCHAR(100) DEFAULT 'PLATFORM_HEURISTIC'"))
        if inspector.has_table("quiz_attempts"):
            cols = [c["name"] for c in inspector.get_columns("quiz_attempts")]
            if "status" not in cols:
                conn.execute(text("ALTER TABLE quiz_attempts ADD COLUMN status VARCHAR(50) DEFAULT 'EVALUATED'"))
            if "feedback_method" not in cols:
                conn.execute(text("ALTER TABLE quiz_attempts ADD COLUMN feedback_method VARCHAR(100) DEFAULT 'Deterministic Pedagogical Feedback'"))
            if "evidence_key" not in cols:
                conn.execute(text("ALTER TABLE quiz_attempts ADD COLUMN evidence_key VARCHAR(255)"))
        conn.commit()

# Create database tables at module load
Base.metadata.create_all(bind=engine)
ensure_db_schema_migrated()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run initial seed check
    seed_initial_data()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS setup
raw_origins = getattr(settings, "ALLOWED_ORIGINS", "")
if isinstance(raw_origins, list):
    allowed_origins = raw_origins
elif isinstance(raw_origins, str) and raw_origins.strip():
    allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
)

from .routers import auth, competencies, assessments, documents, admin_learning, chat, workforce_analytics, voice

# Mount Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(competencies.router, prefix=settings.API_V1_STR)
app.include_router(assessments.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents")
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/content")
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(voice.router, prefix=settings.API_V1_STR)
app.include_router(admin_learning.router)
app.include_router(workforce_analytics.router)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "ecosystem": "MoSPI / NSSTA / iGOT Karmayogi Capacity Building",
        "status": "Online",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

