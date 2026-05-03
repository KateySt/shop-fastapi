from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import MessageType
from app.db.models.base import Base, IDMixin, TimestampMixin


class Message(Base, IDMixin, TimestampMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room: Mapped[str | None] = mapped_column(nullable=True)
    channel: Mapped[str | None] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(default=MessageType.TEXT)

    user = relationship("User", lazy="selectin")
