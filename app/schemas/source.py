from pydantic import BaseModel, Field
from datetime import datetime


class DummySourceOneContentBase(BaseModel):
    stream: str
    topic: str
    image: str
    data: str


class DummySourceOneContentCreate(DummySourceOneContentBase):
    pass


class DummySourceOneContentUpdate(DummySourceOneContentBase):
    pass


class DummySourceOneContentInDBBase(DummySourceOneContentBase):
    id: int
    created_at: datetime


class DummySourceOneContent(DummySourceOneContentInDBBase):
    pass


class DummySourceTwoContentBase(BaseModel):
    stream: str = Field(alias='stream')
    topic: str = Field(alias='topic')
    image: str = Field(alias='image')
    data: str = Field(alias='data')


class DummySourceTwoContentCreate(DummySourceOneContentBase):
    pass


class DummySourceTwoContentUpdate(DummySourceOneContentBase):
    pass


class DummySourceTwoContentInDBBase(DummySourceOneContentBase):
    id: int
    created_at: datetime


class DummySourceTwoContent(DummySourceOneContentInDBBase):
    pass
