from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.repo.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)

    async def get_with_items(self, order_id: UUID) -> Order | None:
        result = await self.session.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    async def get_order_item(self, order_id: UUID, item_id: UUID) -> OrderItem | None:
        result = await self.session.execute(
            select(OrderItem).where(
                OrderItem.order_id == order_id,
                OrderItem.item_id == item_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_order_item(self, order_item: OrderItem) -> OrderItem:
        self.session.add(order_item)
        await self.session.flush()
        await self.session.refresh(order_item)
        return order_item

    async def delete_order_item(self, order_item: OrderItem) -> None:
        await self.session.delete(order_item)
        await self.session.flush()
