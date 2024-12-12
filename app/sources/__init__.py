from typing import List

from pydantic import BaseModel

from .source_one import DummySourceOne
from .source_two import DummySourceTwo
from app.core.config import settings

available_sources = {
    'dummy_source_1': DummySourceOne,
    'dummy_source_2': DummySourceTwo
}


class UserTopics(BaseModel):
    dummy_source_1: List[str] = settings.DS1_AVAILABLE_TOPICS
    dummy_source_2: List[str] = settings.DS2_AVAILABLE_TOPICS
