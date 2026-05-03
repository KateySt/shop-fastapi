from app.db.models import User
from app.db.models.enums import MessageType
from app.dependencies import PaginationParams
from app.mappers import MessageMapper
from app.schemas import HistoryResponseSchema, WSIncomingMessage
from app.services.abstract.abstract_ws_service import AbstractWSService
from app.services.impl.ws_service_impl import WSServiceImpl


class WSService(AbstractWSService):
    def __init__(self, impl: WSServiceImpl, mapper: MessageMapper):
        self.impl = impl
        self.mapper = mapper

    async def handle_message(self, msg: WSIncomingMessage, user: User) -> None:
        user_id = str(user.id)
        match msg.type:
            case MessageType.JOIN:
                await self.impl.handle_join(msg, user_id)
            case MessageType.LEAVE:
                await self.impl.handle_leave(msg, user_id)
            case MessageType.TEXT:
                if msg.payload:
                    await self.impl.handle_text(msg, user)
            case MessageType.PONG:
                pass

    async def get_room_history(
        self,
        room: str,
        pagination: PaginationParams,
    ) -> HistoryResponseSchema:
        messages, total = await self.impl.get_room_history(room, pagination)
        return HistoryResponseSchema(
            messages=[self.mapper.to_response(m) for m in messages],
            total=total,
        )

    async def get_channel_history(
        self,
        channel: str,
        pagination: PaginationParams,
    ) -> HistoryResponseSchema:
        messages, total = await self.impl.get_channel_history(channel, pagination)
        return HistoryResponseSchema(
            messages=[self.mapper.to_response(m) for m in messages],
            total=total,
        )
