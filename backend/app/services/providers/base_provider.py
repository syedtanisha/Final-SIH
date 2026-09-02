import hashlib
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

class IntegrationMode(str, Enum):
    LIVE_API = "LIVE_API"
    LIVE_METADATA = "LIVE_METADATA"
    CURATED_FALLBACK = "CURATED_FALLBACK"
    DISABLED = "DISABLED"

@dataclass
class NormalizedLearningResource:
    internal_resource_key: str
    title: str
    description: str
    provider: str
    publisher_org: str
    source_url: str
    source_type: str
    source_format: str
    access_level: str
    reference_period: Optional[str]
    difficulty_level: str
    estimated_duration_mins: int
    competencies: List[str]
    designation_applicability: List[str]
    department_applicability: List[str]
    provenance_type: str
    last_verified_at: datetime
    dedup_hash: str
    provider_external_id: Optional[str] = None
    verification_level: str = "PORTAL_VERIFIED"  # 'PORTAL_VERIFIED', 'PAGE_VERIFIED', 'RESOURCE_VERIFIED', 'UNVERIFIED'
    mapping_provenance: str = "Platform Curated Competency Mapping"
    thumbnail_url: Optional[str] = None
    version: Optional[str] = None
    publication_date: Optional[str] = None

def compute_dedup_hash(provider: str, source_url: str, title: str, provider_ext_id: Optional[str] = None) -> str:
    norm_prov = (provider or "").strip().upper()
    norm_ext = (provider_ext_id or "").strip().upper()
    norm_url = (source_url or "").strip().lower()
    norm_title = (title or "").strip().lower()
    raw_str = f"{norm_prov}|{norm_ext}|{norm_url}|{norm_title}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

class BaseLearningProvider(ABC):
    def __init__(self, provider_id: str, name: str, default_mode: IntegrationMode = IntegrationMode.CURATED_FALLBACK):
        self.provider_id = provider_id
        self.name = name
        self.integration_mode = default_mode
        self.last_sync_at: Optional[datetime] = None
        self.last_error: Optional[str] = None

    @abstractmethod
    def discover_and_fetch(self) -> List[NormalizedLearningResource]:
        """Fetch and normalize resources from the official learning provider."""
        pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "name": self.name,
            "integration_mode": self.integration_mode.value,
            "last_sync_at": self.last_sync_at.isoformat() if self.last_sync_at else None,
            "last_error": self.last_error
        }
