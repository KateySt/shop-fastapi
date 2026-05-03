from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.db.models.enums import MessageType


class WSIncomingMessage(BaseModel):
    type: MessageType
    payload: str | None = None
    room: str | None = None
    channel: str | None = None


class MessageResponseSchema(BaseModel):
    id: UUID
    type: str
    content: str
    room: str | None = None
    channel: str | None = None
    user_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class HistoryResponseSchema(BaseModel):
    messages: list[MessageResponseSchema]
    total: int
