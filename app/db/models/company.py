from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.item import Item


class Company(Base, IDMixin, TimestampMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    items: Mapped[list[Item]] = relationship(
        "Item", back_populates="company", cascade="all, delete-orphan"
    )
