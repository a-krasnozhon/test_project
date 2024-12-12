from datetime import datetime

from app.db.base_class import MongoBaseModel


class DummySourceOneContent(MongoBaseModel):
    __collection__ = 'dummy_source_1'
    stream: str
    topic: str
    image: str
    data: str
    created_at: datetime


class DummySourceTwoContent(MongoBaseModel):
    __collection__ = 'dummy_source_2'
    stream: str
    topic: str
    image: str
    data: str
    created_at: datetime
