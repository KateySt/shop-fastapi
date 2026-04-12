from uuid import UUID

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.dependencies import PaginationParams, SortingParams
from app.exception import ForbiddenError, NotFoundError
from app.repo.item_repository import ItemRepository
from app.repo.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderUpdate


class OrderServiceImpl:
    def __init__(self, repo: OrderRepository, item_repo: ItemRepository):
        self.repo = repo
        self.item_repo = item_repo

    async def create_order(self, user_id: UUID, data: OrderCreate) -> Order:
        order = Order(user_id=user_id, is_closed=False)
        await self.repo.add(order)

        for order_item_data in data.items:
            item = await self.item_repo.get(order_item_data.item_id)
            if not item:
                raise NotFoundError(f"Item {order_item_data.item_id} not found")

            order_item = OrderItem(
                order_id=order.id,
                item_id=order_item_data.item_id,
                price=item.price,
                quantity=order_item_data.quantity,
            )
            await self.repo.add_order_item(order_item)

        result = await self.repo.get_with_items(order.id)
        if not result:
            raise NotFoundError("Order not found after creation")
        return result

    async def get_order(self, order_id: UUID, user_id: UUID) -> Order:
        order = await self.repo.get_with_items(order_id)
        if not order:
            raise NotFoundError("Order not found")
        if order.user_id != user_id:
            raise ForbiddenError("Access denied")
        return order

    async def list_orders(
        self,
        user_id: UUID,
        pagination: PaginationParams,
        sort: SortingParams,
    ) -> tuple[list[Order], int]:
        orders = await self.repo.list(
            **pagination.to_dict(),
            **sort.to_dict(),
            user_id=user_id,
        )
        total = await self.repo.count_all(user_id=user_id)
        return list(orders), total

    async def update_order(
        self, order_id: UUID, user_id: UUID, data: OrderUpdate
    ) -> Order:
        order = await self.get_order(order_id, user_id)

        if order.is_closed:
            raise ForbiddenError("Cannot update a closed order")

        for order_item in list(order.items):
            await self.repo.delete_order_item(order_item)

        for order_item_data in data.items:
            item = await self.item_repo.get(order_item_data.item_id)
            if not item:
                raise NotFoundError(f"Item {order_item_data.item_id} not found")

            order_item = OrderItem(
                order_id=order.id,
                item_id=order_item_data.item_id,
                price=item.price,
                quantity=order_item_data.quantity,
            )
            await self.repo.add_order_item(order_item)

        result = await self.repo.get_with_items(order.id)
        if not result:
            raise NotFoundError("Order not found after creation")
        return result

    async def delete_order(self, order_id: UUID, user_id: UUID) -> None:
        order = await self.get_order(order_id, user_id)

        if order.is_closed:
            raise ForbiddenError("Cannot delete a closed order")

        await self.repo.delete(order)

    async def close_order(self, order_id: UUID) -> Order:
        order = await self.repo.get_with_items(order_id)

        if not order:
            raise NotFoundError("Order not found")

        if order.is_closed:
            raise ForbiddenError("Order is already closed")

        return await self.repo.update(order, {"is_closed": True})
