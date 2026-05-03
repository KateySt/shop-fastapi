from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.message import Message
from app.repo.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Message)

    async def get_room_history(self, room: str, skip: int, limit: int) -> list[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.room == room)
            .options(selectinload(Message.user))
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_channel_history(
        self, channel: str, skip: int, limit: int
    ) -> list[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.channel == channel)
            .options(selectinload(Message.user))
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
