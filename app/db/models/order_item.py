from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    pass


class OrderItem(Base, IDMixin, TimestampMixin):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    price: Mapped[float] = mapped_column(default=0.0)
    quantity: Mapped[int] = mapped_column(default=0)

    order = relationship("Order", back_populates="items", lazy="selectin")
    item = relationship("Item", lazy="selectin")

    __table_args__ = (UniqueConstraint("order_id", "item_id", name="uq_order_item"),)

    @property
    def total(self):
        return self.price * self.quantity
