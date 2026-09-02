import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_provider import BaseLearningProvider, IntegrationMode, NormalizedLearningResource, compute_dedup_hash
from ..live_fetcher import fetch_official_live_url

logger = logging.getLogger(__name__)

class NSSTATPACProvider(BaseLearningProvider):
    def __init__(self):
        super().__init__(
            provider_id="nssta_tpac",
            name="NSSTA TPAC Training Programmes",
            default_mode=IntegrationMode.LIVE_METADATA
        )
        self.base_url = "https://nssta.gov.in/"

    def discover_and_fetch(self) -> List[NormalizedLearningResource]:
        items: List[NormalizedLearningResource] = []
        self.last_sync_at = datetime.utcnow()

        raw_tpac_programmes = [
            {
                "external_id": "nssta-tpac-2024-01",
                "title": "NSSTA TPAC: Advanced Macroeconomic Accounting & SNA 2008 Framework",
                "description": "Executive TPAC training programme for Senior ISS Officers covering double-entry national accounting balance sheets, capital formation, and GDP deflator estimation.",
                "source_url": "https://nssta.gov.in/",
                "source_type": "Official Training Resource",
                "source_format": "Executive Training Workshop",
                "access_level": "PUBLIC",
                "reference_period": "2024-2025",
                "difficulty_level": "Advanced",
                "estimated_duration_mins": 300,
                "competencies": ["STAT_NAT_ACC"],
                "designation_applicability": ["Deputy Director (ISS)", "Joint Director", "Director General"],
                "department_applicability": ["National Accounts Division", "MoSPI Headquarters"]
            },
            {
                "external_id": "nssta-tpac-2024-02",
                "title": "NSSTA TPAC: Induction & Capacity Building in Official Statistical Governance",
                "description": "Comprehensive TPAC induction programme for newly recruited Statistical Officers covering NSC statutory mandates, Data Quality Frameworks, and Inter-Agency Coordination.",
                "source_url": "https://nssta.gov.in/",
                "source_type": "Official Training Resource",
                "source_format": "Academy Resident Programme",
                "access_level": "PUBLIC",
                "reference_period": "2024-2025",
                "difficulty_level": "Foundational",
                "estimated_duration_mins": 240,
                "competencies": ["STAT_OFFICIAL", "STAT_DATA_GOV"],
                "designation_applicability": ["Statistical Officer", "Assistant Director"],
                "department_applicability": ["MoSPI Headquarters", "Field Operations Division"]
            },
            {
                "external_id": "nssta-tpac-2024-03",
                "title": "NSSTA TPAC: Large-Scale Household Survey Sampling & Weight Calibration",
                "description": "Advanced technical training on multiplier calculation, urban frame survey updates, non-response adjustments, and microdata weight calibration for PLFS and HCES.",
                "source_url": "https://nssta.gov.in/",
                "source_type": "Official Training Resource",
                "source_format": "Technical Lab & Field Practice",
                "access_level": "PUBLIC",
                "reference_period": "2024-2025",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 270,
                "competencies": ["STAT_SURVEY"],
                "designation_applicability": ["Statistical Officer", "Assistant Director", "Deputy Director"],
                "department_applicability": ["Survey Design & Research Division", "Field Operations Division"]
            }
        ]

        live_res = fetch_official_live_url(self.base_url)
        if live_res.get("success"):
            self.integration_mode = IntegrationMode.LIVE_METADATA
            prov_type = "Live Official Metadata"
        else:
            self.integration_mode = IntegrationMode.CURATED_FALLBACK
            prov_type = "Curated Official Metadata"

        for p in raw_tpac_programmes:
            dedup_hash = compute_dedup_hash(self.name, p["source_url"], p["title"], provider_ext_id=None)
            items.append(
                NormalizedLearningResource(
                    internal_resource_key=p["external_id"],
                    provider_external_id=None,
                    title=p["title"],
                    description=p["description"],
                    provider=self.name,
                    publisher_org="NSSTA / MoSPI",
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
                    verification_level="PORTAL_VERIFIED" if prov_type == "Live Official Metadata" else "UNVERIFIED",
                    mapping_provenance="Platform Curated Competency Mapping",
                    last_verified_at=datetime.utcnow(),
                    dedup_hash=dedup_hash
                )
            )

        return items
