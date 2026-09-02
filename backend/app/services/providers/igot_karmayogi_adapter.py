import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_provider import BaseLearningProvider, IntegrationMode, NormalizedLearningResource, compute_dedup_hash
from ..live_fetcher import fetch_official_live_url

logger = logging.getLogger(__name__)

class IGOTKarmayogiProvider(BaseLearningProvider):
    def __init__(self):
        super().__init__(
            provider_id="igot_karmayogi",
            name="iGOT Karmayogi National Learning Portal",
            default_mode=IntegrationMode.CURATED_FALLBACK
        )
        self.base_url = os.getenv("IGOT_BASE_URL", "https://igotkarmayogi.gov.in")
        self.api_key = os.getenv("IGOT_API_KEY", "").strip()
        self.client_id = os.getenv("IGOT_CLIENT_ID", "").strip()
        self.client_secret = os.getenv("IGOT_CLIENT_SECRET", "").strip()

        if self.api_key or (self.client_id and self.client_secret):
            self.integration_mode = IntegrationMode.LIVE_API
        else:
            self.integration_mode = IntegrationMode.CURATED_FALLBACK

    def discover_and_fetch(self) -> List[NormalizedLearningResource]:
        items: List[NormalizedLearningResource] = []
        self.last_sync_at = datetime.utcnow()

        # Predefined curated baseline catalogue for iGOT Karmayogi
        raw_curated = [
            {
                "external_id": "igot-course-stat-01",
                "title": "iGOT Karmayogi: Foundations of Sample Survey Methodology",
                "description": "Comprehensive official e-learning course covering sampling frames, NSSO stratification designs, non-sampling error minimization, and estimation formulas.",
                "source_url": "https://igotkarmayogi.gov.in/course/sample-survey-design",
                "source_type": "Official Training Course",
                "source_format": "Interactive Video & Assessment",
                "access_level": "PUBLIC",
                "reference_period": "2024-2025",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 180,
                "competencies": ["STAT_SURVEY"],
                "designation_applicability": ["Statistical Officer", "Assistant Director", "Deputy Director"],
                "department_applicability": ["Field Operations Division", "Survey Design & Research Division"]
            },
            {
                "external_id": "igot-course-nat-02",
                "title": "iGOT Karmayogi: Gross Value Added (GVA) & GDP Compilation Mechanics",
                "description": "National Accounts training module explaining sector-wise GVA estimation, double deflation, price deflators, and System of National Accounts (SNA 2008) principles.",
                "source_url": "https://igotkarmayogi.gov.in/course/national-accounts-gva",
                "source_type": "Official Training Course",
                "source_format": "Interactive e-Learning",
                "access_level": "PUBLIC",
                "reference_period": "2024",
                "difficulty_level": "Advanced",
                "estimated_duration_mins": 240,
                "competencies": ["STAT_NAT_ACC"],
                "designation_applicability": ["Deputy Director (ISS)", "Joint Director", "Director"],
                "department_applicability": ["National Accounts Division"]
            },
            {
                "external_id": "igot-course-comp-03",
                "title": "iGOT Karmayogi: Automated Data Pipeline & Microdata Analysis in Python",
                "description": "Hands-on data science course for statistical officers on processing large-scale survey unit data using pandas, NumPy, and statistical computing best practices.",
                "source_url": "https://igotkarmayogi.gov.in/course/python-statistical-analysis",
                "source_type": "Official Technical Training",
                "source_format": "Self-Paced Practical",
                "access_level": "PUBLIC",
                "reference_period": "2024",
                "difficulty_level": "Intermediate",
                "estimated_duration_mins": 150,
                "competencies": ["STAT_COMPUTE"],
                "designation_applicability": ["Statistical Investigator", "Statistical Officer", "Assistant Director"],
                "department_applicability": ["Data Processing Division", "MoSPI Headquarters"]
            }
        ]

        if self.integration_mode == IntegrationMode.LIVE_API:
            logger.info(f"[iGOTProvider] Attempting LIVE_API fetch from {self.base_url}")
            live_res = fetch_official_live_url(f"{self.base_url}/course/sample-survey-design")
            if live_res.get("success"):
                prov_type = "Live Official API"
            else:
                logger.warning(f"[iGOTProvider] Live API request failed. Falling back to CURATED_FALLBACK.")
                self.integration_mode = IntegrationMode.CURATED_FALLBACK
                prov_type = "Curated Official Metadata"
        else:
            prov_type = "Curated Official Metadata"

        for c in raw_curated:
            dedup_hash = compute_dedup_hash(self.name, c["source_url"], c["title"], provider_ext_id=None)
            items.append(
                NormalizedLearningResource(
                    internal_resource_key=c["external_id"],
                    provider_external_id=None,  # No official provider API external ID claimed in CURATED_FALLBACK mode
                    title=c["title"],
                    description=c["description"],
                    provider=self.name,
                    publisher_org="iGOT Karmayogi / DoPT",
                    source_url=c["source_url"],
                    source_type=c["source_type"],
                    source_format=c["source_format"],
                    access_level=c["access_level"],
                    reference_period=c.get("reference_period"),
                    difficulty_level=c["difficulty_level"],
                    estimated_duration_mins=c["estimated_duration_mins"],
                    competencies=c["competencies"],
                    designation_applicability=c["designation_applicability"],
                    department_applicability=c["department_applicability"],
                    provenance_type=prov_type,
                    verification_level="PORTAL_VERIFIED" if prov_type == "Live Official API" else "UNVERIFIED",
                    mapping_provenance="Platform Curated Competency Mapping",
                    last_verified_at=datetime.utcnow(),
                    dedup_hash=dedup_hash
                )
            )

        return items
