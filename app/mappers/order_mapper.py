from app.db.models.order import Order
from app.mappers.base_mapper import BaseMapper
from app.mappers.paginated_mapper import PaginatedMapper
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse, OrderUpdate


class OrderMapper(BaseMapper[Order, OrderCreate, OrderUpdate, OrderResponse]):
    def __init__(self):
        super().__init__(orm_class=Order, response_class=OrderResponse)


class OrderPaginatedMapper(PaginatedMapper[Order, OrderListResponse]):
    def __init__(self):
        super().__init__(
            orm_class=Order,
            response_class=OrderListResponse,
            item_schema=OrderResponse,
        )
