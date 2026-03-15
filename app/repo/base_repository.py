import uuid
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception.custom_error import AlreadyExistsError

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, obj_id: uuid.UUID) -> T | None:
        return await self.session.get(self.model, obj_id)

    async def list(self, skip: int = 0, limit: int = 20, **filters) -> Sequence[T]:
        query = select(self.model)

        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)

        result = await self.session.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def add(self, obj: T) -> T:
        try:
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            raise AlreadyExistsError(
                "Object with this unique field already exists"
            ) from e

    async def update(self, obj: T, data: dict) -> T:
        for field, value in data.items():
            setattr(obj, field, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T):
        await self.session.delete(obj)
        await self.session.flush()

    async def count_all(self, **filters) -> int:
        query = select(func.count()).select_from(self.model)

        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)

        result = await self.session.execute(query)
        return result.scalar_one()
