from abc import ABC, abstractmethod

from app.db.models import User
from app.dependencies import PaginationParams
from app.schemas import HistoryResponseSchema, WSIncomingMessage


class AbstractWSService(ABC):

    @abstractmethod
    async def handle_message(self, msg: WSIncomingMessage, user: User) -> None: ...

    @abstractmethod
    async def get_room_history(
        self,
        room: str,
        pagination: PaginationParams,
    ) -> HistoryResponseSchema: ...

    @abstractmethod
    async def get_channel_history(
        self,
        channel: str,
        pagination: PaginationParams,
    ) -> HistoryResponseSchema: ...
