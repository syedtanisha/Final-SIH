import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.models import LearningResource, Competency, ResourceCompetencyMapping
from ..services.live_fetcher import is_official_domain
from .providers import PROVIDER_REGISTRY, BaseLearningProvider, NormalizedLearningResource

logger = logging.getLogger(__name__)

def synchronize_provider(provider_id: str, db: Session) -> Dict[str, Any]:
    provider = PROVIDER_REGISTRY.get(provider_id)
    if not provider:
        raise ValueError(f"Unknown provider '{provider_id}'. Available: {list(PROVIDER_REGISTRY.keys())}")

    errors: List[str] = []
    items_ingested = 0
    items_updated = 0
    duplicates_skipped = 0
    provenance_counts: Dict[str, int] = {}

    all_competencies = {c.code: c for c in db.query(Competency).all()}

    try:
        norm_items: List[NormalizedLearningResource] = provider.discover_and_fetch()
    except Exception as e:
        logger.error(f"[SyncService] Error fetching from provider '{provider_id}': {e}", exc_info=True)
        provider.last_error = str(e)
        return {
            "provider_id": provider.provider_id,
            "provider_name": provider.name,
            "integration_mode": provider.integration_mode.value,
            "status": "error",
            "total_fetched": 0,
            "items_ingested": 0,
            "items_updated": 0,
            "duplicates_skipped": 0,
            "last_verified_at": datetime.utcnow().isoformat(),
            "provenance_breakdown": {},
            "errors": [str(e)]
        }

    provider.last_sync_at = datetime.utcnow()
    provider.last_error = None

    for item in norm_items:
        # 1. Validation
        if not item.title or not item.source_url:
            errors.append(f"Skipped item with missing title or source URL.")
            continue

        if not is_official_domain(item.source_url):
            errors.append(f"Skipped item '{item.title}' due to unverified non-official domain.")
            continue

        prov_type = item.provenance_type or "Curated Official Metadata"
        provenance_counts[prov_type] = provenance_counts.get(prov_type, 0) + 1

        # 2. Deduplication Strategy: (a) official_url, (b) dedup_hash
        existing = db.query(LearningResource).filter(
            (LearningResource.official_url == item.source_url) |
            (LearningResource.dedup_hash == item.dedup_hash)
        ).first()

        role_rel = ",".join(item.designation_applicability) if item.designation_applicability else "all"

        if existing:
            # Update existing resource metadata without duplicating
            existing.title = item.title
            existing.description = item.description
            existing.source = item.provider
            existing.publisher_org = item.publisher_org
            existing.provenance_type = item.provenance_type
            existing.reference_period = item.reference_period
            existing.resource_type = item.source_type
            existing.source_format = item.source_format
            existing.access_level = item.access_level
            existing.difficulty = item.difficulty_level
            existing.estimated_duration_mins = item.estimated_duration_mins
            existing.dedup_hash = item.dedup_hash
            existing.last_verified_at = datetime.utcnow()
            existing.role_relevance = role_rel
            existing.provider_external_id = item.provider_external_id
            existing.verification_level = item.verification_level

            res_obj = existing
            items_updated += 1
        else:
            # Ingest new resource
            res_obj = LearningResource(
                title=item.title,
                description=item.description,
                source=item.provider,
                official_url=item.source_url,
                resource_type=item.source_type,
                difficulty=item.difficulty_level,
                estimated_duration_mins=item.estimated_duration_mins,
                publisher_org=item.publisher_org,
                provenance_type=item.provenance_type,
                reference_period=item.reference_period,
                access_level=item.access_level,
                source_format=item.source_format,
                dedup_hash=item.dedup_hash,
                last_verified_at=datetime.utcnow(),
                role_relevance=role_rel,
                provider_external_id=item.provider_external_id,
                verification_level=item.verification_level,
                is_active=True
            )
            db.add(res_obj)
            db.flush()
            items_ingested += 1

        # 3. Competency Mapping Alignment
        if item.competencies:
            for code in item.competencies:
                comp = all_competencies.get(code)
                if comp:
                    existing_map = db.query(ResourceCompetencyMapping).filter(
                        ResourceCompetencyMapping.resource_id == res_obj.id,
                        ResourceCompetencyMapping.competency_id == comp.id
                    ).first()
                    if not existing_map:
                        mapping = ResourceCompetencyMapping(
                            resource_id=res_obj.id,
                            competency_id=comp.id,
                            relevance_score=1.0,
                            mapping_provenance=item.mapping_provenance
                        )
                        db.add(mapping)
                    else:
                        existing_map.mapping_provenance = item.mapping_provenance

    db.commit()

    return {
        "provider_id": provider.provider_id,
        "provider_name": provider.name,
        "integration_mode": provider.integration_mode.value,
        "status": "success",
        "total_fetched": len(norm_items),
        "items_ingested": items_ingested,
        "items_updated": items_updated,
        "duplicates_skipped": duplicates_skipped,
        "last_verified_at": provider.last_sync_at.isoformat(),
        "provenance_breakdown": provenance_counts,
        "errors": errors
    }

def synchronize_all_providers(db: Session) -> List[Dict[str, Any]]:
    results = []
    for pid in PROVIDER_REGISTRY.keys():
        results.append(synchronize_provider(pid, db))
    return results

def get_all_provider_statuses(db: Session) -> List[Dict[str, Any]]:
    statuses = []
    for pid, provider in PROVIDER_REGISTRY.items():
        res_count = db.query(LearningResource).filter(LearningResource.source == provider.name).count()
        st = provider.get_status()
        st["resource_count"] = res_count
        statuses.append(st)
    return statuses
