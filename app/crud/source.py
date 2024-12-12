from app.crud.base import CRUDBase
from app.models import DummySourceOneContent
from app.schemas.source import (
    DummySourceOneContentUpdate, DummySourceOneContentCreate
)


class CRUDSource(CRUDBase[DummySourceOneContent, DummySourceOneContentUpdate, DummySourceOneContentCreate
                 ]):
    model = DummySourceOneContent

    async def get_topic(self, topic: str):
        return await self.collection.find({'topic': topic})
