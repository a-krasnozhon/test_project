from datetime import datetime

from app.db.base_class import MongoBaseModel


class Stream(MongoBaseModel):
    __collection__ = 'stream'

    stream: str
    topic: str
    image: str
    data: str

    created_at: datetime
