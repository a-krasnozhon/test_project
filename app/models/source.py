from datetime import datetime

from pydantic import BaseModel


class DummySourceOneContent(BaseModel):
    __collection__ = 'dummy_source_1'
    stream: str
    topic: str
    image: str
    data: str
    created_at: datetime


class DummySourceTwoContent(BaseModel):
    __collection__ = 'dummy_source_2'
    stream: str
    topic: str
    image: str
    data: str
    created_at: datetime
