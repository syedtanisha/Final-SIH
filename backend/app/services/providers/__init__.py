from typing import Dict
from .base_provider import BaseLearningProvider, IntegrationMode, NormalizedLearningResource
from .igot_karmayogi_adapter import IGOTKarmayogiProvider
from .nssta_tpac_adapter import NSSTATPACProvider
from .mospi_publications_adapter import MoSPIPublicationsProvider
from .esankhyiki_datasets_adapter import ESankhyikiDatasetsProvider

PROVIDER_REGISTRY: Dict[str, BaseLearningProvider] = {
    "igot_karmayogi": IGOTKarmayogiProvider(),
    "nssta_tpac": NSSTATPACProvider(),
    "mospi_publications": MoSPIPublicationsProvider(),
    "esankhyiki_datasets": ESankhyikiDatasetsProvider()
}

def get_provider(provider_id: str) -> BaseLearningProvider:
    provider = PROVIDER_REGISTRY.get(provider_id)
    if not provider:
        raise ValueError(f"Unknown learning provider ID '{provider_id}'. Available: {list(PROVIDER_REGISTRY.keys())}")
    return provider
