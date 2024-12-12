from app.sources.base_schema import SourceBase
from app.core.config import settings


class DummySourceOne(SourceBase):
    name: str = 'dummy_source_1'
    base_url: str = settings.DS1_BASE_URL
    subscription_url: str = settings.DS1_SUBSCRIBE
    data_fetch_url: str = settings.DS1_RETRIEVE
    topics: str = settings.DS1_AVAILABLE_TOPICS
    description: str = settings.DS1_DESCRIPTION
