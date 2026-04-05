from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer, Numeric

from app.db.models.base import Base, IDMixin, TimestampMixin
from app.db.models.enums import Currency

if TYPE_CHECKING:
    from app.db.models.company import Company


class Item(Base, IDMixin, TimestampMixin):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False, default=Decimal("0.00")
    )
    currency: Mapped[Currency] = mapped_column(
        SAEnum(Currency, name="currency_enum"),
        nullable=False,
        default=Currency.UAH,
    )
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )

    company: Mapped[Company] = relationship("Company", back_populates="items")
