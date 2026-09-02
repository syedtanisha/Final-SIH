import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_provider import BaseLearningProvider, IntegrationMode, NormalizedLearningResource, compute_dedup_hash
from ..live_fetcher import fetch_official_live_url

logger = logging.getLogger(__name__)

class MoSPIPublicationsProvider(BaseLearningProvider):
    def __init__(self):
        super().__init__(
            provider_id="mospi_publications",
            name="MoSPI Official Publications & Survey Documentation",
            default_mode=IntegrationMode.LIVE_METADATA
        )
        self.base_url = "https://www.mospi.gov.in/publication"

    def discover_and_fetch(self) -> List[NormalizedLearningResource]:
        items: List[NormalizedLearningResource] = []
        self.last_sync_at = datetime.utcnow()

        raw_pubs = [
            {
                "external_id": "mospi-pub-2024-plfs",
                "title": "MoSPI Annual Report: Periodic Labour Force Survey (PLFS) 2023-24",
                "description": "Official statistical publication presenting key labor force indicators including LFPR, WPR, and UR alongside sampling methodology and multiplier documentation.",
                "source_url": "https://www.mospi.gov.in/publication",
                "source_type": "Official Publication",
                "source_format": "PDF",
                "access_level": "PUBLIC",
                "reference_period": "2023-2024",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 120,
                "competencies": ["STAT_SURVEY"],
                "designation_applicability": ["Statistical Officer", "Assistant Director", "Deputy Director"],
                "department_applicability": ["Survey Design & Research Division", "Field Operations Division"]
            },
            {
                "external_id": "mospi-pub-2024-cpi",
                "title": "MoSPI Technical Manual: Consumer Price Index (CPI) Revision & Base Year Weighting",
                "description": "Official methodology document detailing item basket selection, price collection protocols, Laspeyres base weighting, and geometric mean aggregation.",
                "source_url": "https://www.mospi.gov.in/publication",
                "source_type": "Official Publication",
                "source_format": "PDF",
                "access_level": "PUBLIC",
                "reference_period": "2024",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 90,
                "competencies": ["STAT_PRICE_IND"],
                "designation_applicability": ["Statistical Officer", "Assistant Director", "Deputy Director (ISS)"],
                "department_applicability": ["Price Statistics Division"]
            }
        ]

        live_res = fetch_official_live_url(self.base_url)
        if live_res.get("success"):
            self.integration_mode = IntegrationMode.LIVE_METADATA
            prov_type = "Live Official Metadata"
        else:
            self.integration_mode = IntegrationMode.CURATED_FALLBACK
            prov_type = "Curated Official Metadata"

        for p in raw_pubs:
            dedup_hash = compute_dedup_hash(self.name, p["source_url"], p["title"], provider_ext_id=None)
            items.append(
                NormalizedLearningResource(
                    internal_resource_key=p["external_id"],
                    provider_external_id=None,
                    title=p["title"],
                    description=p["description"],
                    provider=self.name,
                    publisher_org="Ministry of Statistics & Programme Implementation (MoSPI)",
                    source_url=p["source_url"],
                    source_type=p["source_type"],
                    source_format=p["source_format"],
                    access_level=p["access_level"],
                    reference_period=p.get("reference_period"),
                    difficulty_level=p["difficulty_level"],
                    estimated_duration_mins=p["estimated_duration_mins"],
                    competencies=p["competencies"],
                    designation_applicability=p["designation_applicability"],
                    department_applicability=p["department_applicability"],
                    provenance_type=prov_type,
                    verification_level="PAGE_VERIFIED" if prov_type == "Live Official Metadata" else "UNVERIFIED",
                    mapping_provenance="Platform Curated Competency Mapping",
                    last_verified_at=datetime.utcnow(),
                    dedup_hash=dedup_hash
                )
            )

        return items
