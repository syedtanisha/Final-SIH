import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_provider import BaseLearningProvider, IntegrationMode, NormalizedLearningResource, compute_dedup_hash
from ..live_fetcher import fetch_official_live_url

logger = logging.getLogger(__name__)

class ESankhyikiDatasetsProvider(BaseLearningProvider):
    def __init__(self):
        super().__init__(
            provider_id="esankhyiki_datasets",
            name="eSankhyiki Official Datasets & Time-Series",
            default_mode=IntegrationMode.LIVE_METADATA
        )
        self.base_url = "https://esankhyiki.mospi.gov.in/macroindicators-main"

    def discover_and_fetch(self) -> List[NormalizedLearningResource]:
        items: List[NormalizedLearningResource] = []
        self.last_sync_at = datetime.utcnow()

        raw_datasets = [
            {
                "external_id": "esankhyiki-ds-01",
                "title": "eSankhyiki Macro Indicators: National Accounts & GDP Time-Series Data",
                "description": "Official macroeconomic time-series dataset covering GDP at basic prices, GVA by economic activity, and expenditure components downloadable in CSV format.",
                "source_url": "https://esankhyiki.mospi.gov.in/macroindicators-main",
                "source_type": "Official Public Data",
                "source_format": "CSV",
                "access_level": "PUBLIC",
                "reference_period": "2011-12 to 2024-25",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 90,
                "competencies": ["STAT_NAT_ACC"],
                "designation_applicability": ["Deputy Director (ISS)", "Joint Director", "Director"],
                "department_applicability": ["National Accounts Division"]
            },
            {
                "external_id": "esankhyiki-ds-02",
                "title": "eSankhyiki Data Catalogue: All-India Official Statistical Datasets Index",
                "description": "Single-window national catalogue for discovering publicly available MoSPI survey datasets, census aggregations, and indicator tables with downloadable Excel metadata.",
                "source_url": "https://esankhyiki.mospi.gov.in/catalogue-main",
                "source_type": "Official Metadata",
                "source_format": "Excel",
                "access_level": "PUBLIC",
                "reference_period": "2024",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 60,
                "competencies": ["STAT_DATA_GOV"],
                "designation_applicability": ["Statistical Officer", "Assistant Director", "Deputy Director"],
                "department_applicability": ["MoSPI Headquarters"]
            }
        ]

        live_res = fetch_official_live_url(self.base_url)
        if live_res.get("success"):
            self.integration_mode = IntegrationMode.LIVE_METADATA
            prov_type = "Live Official Metadata"
        else:
            self.integration_mode = IntegrationMode.CURATED_FALLBACK
            prov_type = "Curated Official Metadata"

        for d in raw_datasets:
            dedup_hash = compute_dedup_hash(self.name, d["source_url"], d["title"], provider_ext_id=None)
            items.append(
                NormalizedLearningResource(
                    internal_resource_key=d["external_id"],
                    provider_external_id=None,
                    title=d["title"],
                    description=d["description"],
                    provider=self.name,
                    publisher_org="eSankhyiki",
                    source_url=d["source_url"],
                    source_type=d["source_type"],
                    source_format=d["source_format"],
                    access_level=d["access_level"],
                    reference_period=d.get("reference_period"),
                    difficulty_level=d["difficulty_level"],
                    estimated_duration_mins=d["estimated_duration_mins"],
                    competencies=d["competencies"],
                    designation_applicability=d["designation_applicability"],
                    department_applicability=d["department_applicability"],
                    provenance_type=prov_type,
                    verification_level="RESOURCE_VERIFIED" if prov_type == "Live Official Metadata" else "UNVERIFIED",
                    mapping_provenance="Platform Curated Competency Mapping",
                    last_verified_at=datetime.utcnow(),
                    dedup_hash=dedup_hash
                )
            )

        return items
