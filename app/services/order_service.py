from uuid import UUID

from app.db.models import User
from app.dependencies import PaginationParams, SortingParams
from app.mappers import OrderMapper, OrderPaginatedMapper
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse, OrderUpdate
from app.services.abstract import AbstractOrderService
from app.services.impl.order_service_impl import OrderServiceImpl


class OrderService(AbstractOrderService):
    def __init__(
        self,
        impl: OrderServiceImpl,
        mapper: OrderMapper,
        paginated_mapper: OrderPaginatedMapper,
    ):
        self.impl = impl
        self.mapper = mapper
        self.paginated_mapper = paginated_mapper

    async def create_order(self, user: User, data: OrderCreate) -> OrderResponse:
        orm = await self.impl.create_order(user.id, data)
        return self.mapper.to_response(orm)

    async def get_order(self, order_id: UUID, user: User) -> OrderResponse:
        orm = await self.impl.get_order(order_id, user.id)
        return self.mapper.to_response(orm)

    async def list_orders(
        self, user: User, pagination: PaginationParams, sort: SortingParams
    ) -> OrderListResponse:
        orders, total = await self.impl.list_orders(user.id, pagination, sort)
        return self.paginated_mapper.from_orm_list(
            orm_list=orders, total=total, pagination=pagination
        )

    async def update_order(
        self, order_id: UUID, user: User, data: OrderUpdate
    ) -> OrderResponse:
        orm = await self.impl.update_order(order_id, user.id, data)
        return self.mapper.to_response(orm)

    async def delete_order(self, order_id: UUID, user: User) -> None:
        await self.impl.delete_order(order_id, user.id)

    async def close_order(self, order_id: UUID) -> OrderResponse:
        orm = await self.impl.close_order(order_id)
        return self.mapper.to_response(orm)
