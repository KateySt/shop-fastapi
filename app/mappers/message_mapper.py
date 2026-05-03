from app.db.models.message import Message
from app.mappers.base_mapper import BaseMapper
from app.schemas import MessageResponseSchema, WSIncomingMessage


class MessageMapper(
    BaseMapper[Message, WSIncomingMessage, WSIncomingMessage, MessageResponseSchema]
):
    def __init__(self):
        super().__init__(
            orm_class=Message,
            response_class=MessageResponseSchema,
        )

    def from_create(self, dto: WSIncomingMessage, **extra) -> Message:
        return Message(
            content=dto.payload,
            room=dto.room,
            channel=dto.channel,
            type=dto.type,
            **extra,
        )
