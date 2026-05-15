from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ModelType:
        instance = self.model(**data)

        self.db.add(instance)

        await self.db.flush()
        await self.db.refresh(instance)

        return instance

    async def get_by_id(self, item_id: int) -> ModelType | None:
        query = select(self.model).where(
            self.model.id == item_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def update(
        self,
        instance: ModelType,
        data: dict,
    ) -> ModelType:
        for field, value in data.items():
            setattr(instance, field, value)

        await self.db.flush()
        await self.db.refresh(instance)

        return instance