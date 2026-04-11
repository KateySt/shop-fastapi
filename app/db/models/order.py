from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    pass


class Order(Base, IDMixin, TimestampMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_closed: Mapped[bool] = mapped_column(default=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", lazy="selectin")

    @property
    def cost(self):
        return sum([item.total for item in self.items])
