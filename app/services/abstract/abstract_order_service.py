from abc import ABC, abstractmethod
from uuid import UUID

from app.db.models import User
from app.dependencies import PaginationParams, SortingParams
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse, OrderUpdate


class AbstractOrderService(ABC):

    @abstractmethod
    async def create_order(self, user: User, data: OrderCreate) -> OrderResponse: ...

    @abstractmethod
    async def get_order(self, order_id: UUID, user: User) -> OrderResponse: ...

    @abstractmethod
    async def list_orders(
        self, user: User, pagination: PaginationParams, sort: SortingParams
    ) -> OrderListResponse: ...

    @abstractmethod
    async def update_order(
        self, order_id: UUID, user: User, data: OrderUpdate
    ) -> OrderResponse: ...

    @abstractmethod
    async def delete_order(self, order_id: UUID, user: User) -> None: ...

    @abstractmethod
    async def close_order(self, order_id: UUID) -> OrderResponse: ...
