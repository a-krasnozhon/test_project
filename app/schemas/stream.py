from typing import Optional, List

from pydantic import BaseModel


class StreamBase(BaseModel):
    email: str
    username: Optional[str] = None
    topics: List[str]


class StreamUpdate(StreamBase):
    pass


class StreamCreate(StreamBase):
    pass


class StreamInDBBase(StreamBase):
    id: int


class Stream(StreamInDBBase):
    pass
