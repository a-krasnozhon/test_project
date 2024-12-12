from app.sources.base_schema import SourceBase
from app.core.config import settings


class DummySourceTwo(SourceBase):
    name: str = 'dummy_source_2'
    base_url: str = settings.DS2_BASE_URL
    subscription_url: str = settings.DS2_SUBSCRIBE
    data_fetch_url: str = settings.DS2_RETRIEVE
    topics: str = settings.DS2_AVAILABLE_TOPICS
    description: str = settings.DS2_DESCRIPTION
