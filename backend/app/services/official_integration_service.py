import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.models import OfficialSource, LearningResource, Competency, ResourceCompetencyMapping
from .source_adapters import ADAPTER_REGISTRY, BaseSourceAdapter

logger = logging.getLogger(__name__)

OFFICIAL_SOURCES_REGISTRY_SEED = [
    {
        "source_id": "mospi_esankhyiki_macro",
        "name": "eSankhyiki Macroeconomic Indicators Portal",
        "organization": "eSankhyiki",
        "base_url": "https://esankhyiki.mospi.gov.in/macroindicators-main",
        "source_type": "Official Public Data",
        "access_method": "Downloadable CSV",
        "authentication_required": False,
        "access_level": "PUBLIC"
    },
    {
        "source_id": "mospi_esankhyiki_catalogue",
        "name": "eSankhyiki Data Catalogue Index",
        "organization": "eSankhyiki",
        "base_url": "https://esankhyiki.mospi.gov.in/catalogue-main",
        "source_type": "Official Metadata",
        "access_method": "Dataset Catalogue",
        "authentication_required": False,
        "access_level": "PUBLIC"
    },
    {
        "source_id": "nssta_training_portal",
        "name": "NSSTA Official Training Academy Curricula",
        "organization": "NSSTA",
        "base_url": "https://nssta.gov.in/",
        "source_type": "Official Training Resource",
        "access_method": "Training Resource",
        "authentication_required": False,
        "access_level": "PUBLIC"
    },
    {
        "source_id": "mospi_publications_portal",
        "name": "MoSPI Official Statistical Publications & Survey Documentation",
        "organization": "MoSPI",
        "base_url": "https://www.mospi.gov.in/publication",
        "source_type": "Official Metadata",
        "access_method": "Publication",
        "authentication_required": False,
        "access_level": "PUBLIC"
    },
    {
        "source_id": "mospi_unitdata_library",
        "name": "MoSPI UnitData API Client & Microdata Governance",
        "organization": "MoSPI",
        "base_url": "https://www.mospi.gov.in/unitdata-python-library",
        "source_type": "Restricted Data",
        "access_method": "Official API",
        "authentication_required": True,
        "access_level": "REGISTERED"
    }
]

def seed_official_sources(db: Session) -> List[OfficialSource]:
    sources: List[OfficialSource] = []
    for s_data in OFFICIAL_SOURCES_REGISTRY_SEED:
        existing = db.query(OfficialSource).filter(OfficialSource.source_id == s_data["source_id"]).first()
        if not existing:
            source_obj = OfficialSource(
                source_id=s_data["source_id"],
                name=s_data["name"],
                organization=s_data["organization"],
                base_url=s_data["base_url"],
                source_type=s_data["source_type"],
                access_method=s_data["access_method"],
                authentication_required=s_data["authentication_required"],
                access_level=s_data["access_level"],
                enabled=True,
                last_checked_at=datetime.utcnow()
            )
            db.add(source_obj)
            db.commit()
            db.refresh(source_obj)
            sources.append(source_obj)
        else:
            sources.append(existing)
    return sources

def get_registered_sources(db: Session) -> List[OfficialSource]:
    sources = db.query(OfficialSource).all()
    if not sources:
        sources = seed_official_sources(db)
    return sources

def refresh_official_sources(db: Session, target_source_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    sources = get_registered_sources(db)
    if target_source_ids:
        sources = [s for s in sources if s.source_id in target_source_ids]

    all_competencies = {c.code: c for c in db.query(Competency).all()}

    summary = {
        "total_sources_processed": 0,
        "items_discovered": 0,
        "items_ingested": 0,
        "items_updated": 0,
        "duplicates_skipped": 0,
        "errors": []
    }

    for source in sources:
        if not source.enabled:
            continue

        adapter_cls = ADAPTER_REGISTRY.get(source.source_id)
        if not adapter_cls:
            logger.warning(f"[OfficialIntegration] No adapter registered for source_id '{source.source_id}'")
            continue

        source_info = {
            "source_id": source.source_id,
            "name": source.name,
            "organization": source.organization,
            "base_url": source.base_url,
            "source_type": source.source_type,
            "access_method": source.access_method,
            "access_level": source.access_level
        }

        try:
            adapter: BaseSourceAdapter = adapter_cls(source_info)
            discovered_items = adapter.discover_and_fetch()
            summary["total_sources_processed"] += 1
            summary["items_discovered"] += len(discovered_items)

            for raw_item in discovered_items:
                if not adapter.validate_item(raw_item):
                    summary["errors"].append(f"Validation failed for raw item '{raw_item.get('title')}' from {source.source_id}")
                    continue

                norm_item = adapter.normalize_item(raw_item)
                dedup_hash = norm_item["dedup_hash"]

                existing_resource = db.query(LearningResource).filter(
                    (LearningResource.dedup_hash == dedup_hash) | (LearningResource.official_url == norm_item["official_url"])
                ).first()

                if existing_resource:
                    # Idempotent update
                    existing_resource.dedup_hash = dedup_hash
                    existing_resource.provenance_type = norm_item["provenance_type"]
                    existing_resource.last_verified_at = datetime.utcnow()
                    existing_resource.version = norm_item.get("version") or existing_resource.version
                    existing_resource.publication_date = norm_item.get("publication_date") or existing_resource.publication_date
                    existing_resource.source_id = source.id
                    summary["items_updated"] += 1
                    summary["duplicates_skipped"] += 1
                else:
                    # Ingest new official resource
                    new_resource = LearningResource(
                        title=norm_item["title"],
                        description=norm_item["description"],
                        source=norm_item["source"],
                        official_url=norm_item["official_url"],
                        resource_type=norm_item["resource_type"],
                        difficulty=norm_item["difficulty"],
                        estimated_duration_mins=norm_item["estimated_duration_mins"],
                        publisher_org=norm_item["publisher_org"],
                        provenance_type=norm_item["provenance_type"],
                        reference_period=norm_item["reference_period"],
                        thumbnail_url=norm_item["thumbnail_url"],
                        is_active=True,
                        source_id=source.id,
                        source_format=norm_item["source_format"],
                        access_level=norm_item["access_level"],
                        publication_date=norm_item["publication_date"],
                        version=norm_item["version"],
                        dedup_hash=dedup_hash,
                        last_verified_at=datetime.utcnow(),
                        role_relevance=norm_item["role_relevance"]
                    )
                    db.add(new_resource)
                    db.flush()

                    comp_code = norm_item.get("competency_code")
                    if comp_code and comp_code in all_competencies:
                        mapping = ResourceCompetencyMapping(
                            resource_id=new_resource.id,
                            competency_id=all_competencies[comp_code].id,
                            relevance_score=1.0
                        )
                        db.add(mapping)

                    summary["items_ingested"] += 1

            source.last_checked_at = datetime.utcnow()
            db.commit()
        except Exception as e:
            db.rollback()
            err_msg = f"[OfficialIntegration] Error processing source '{source.source_id}': {str(e)}"
            logger.error(err_msg)
            summary["errors"].append(err_msg)

    return summary
