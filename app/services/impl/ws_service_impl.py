from app.db.models import User
from app.db.models.enums import MessageType
from app.db.models.message import Message
from app.dependencies import PaginationParams
from app.repo import MessageRepository
from app.websockets.connection_manager import ConnectionManager


class WSServiceImpl:
    def __init__(self, repo: MessageRepository, manager: ConnectionManager):
        self.repo = repo
        self.manager = manager

    async def handle_join(self, msg, user_id: str) -> None:
        if msg.room:
            self.manager.join_room(user_id, msg.room)
            await self.manager.broadcast_to_room(
                msg.room,
                {"type": "join", "payload": f"User {user_id} joined", "room": msg.room},
            )
        if msg.channel:
            self.manager.subscribe(user_id, msg.channel)

    async def handle_leave(self, msg, user_id: str) -> None:
        if msg.room:
            self.manager.leave_room(user_id, msg.room)
            await self.manager.broadcast_to_room(
                msg.room,
                {"type": "leave", "payload": f"User {user_id} left", "room": msg.room},
                exclude_user=user_id,
            )
        if msg.channel:
            self.manager.unsubscribe(user_id, msg.channel)

    async def handle_text(self, msg, user: User) -> Message:
        db_msg = Message(
            user_id=user.id,
            room=msg.room,
            channel=msg.channel,
            content=msg.payload,
            type=MessageType.TEXT,
        )
        await self.repo.add(db_msg)
        await self.repo.session.commit()

        out = {
            "type": "text",
            "payload": msg.payload,
            "from_user": str(user.id),
        }
        if msg.room:
            out["room"] = msg.room
            await self.manager.broadcast_to_room(
                msg.room, out, exclude_user=str(user.id)
            )
        elif msg.channel:
            out["channel"] = msg.channel
            await self.manager.broadcast_to_channel(
                msg.channel, out, exclude_user=str(user.id)
            )

        return db_msg

    async def get_room_history(
        self,
        room: str,
        pagination: PaginationParams,
    ) -> tuple[list[Message], int]:
        messages = await self.repo.get_room_history(room, **pagination.to_dict())
        total = await self.repo.count_all(room=room)
        return messages, total

    async def get_channel_history(
        self,
        channel: str,
        pagination: PaginationParams,
    ) -> tuple[list[Message], int]:
        messages = await self.repo.get_channel_history(channel, **pagination.to_dict())
        total = await self.repo.count_all(channel=channel)
        return messages, total
