import datetime

from sqlalchemy import ARRAY, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base, IDMixin, TimestampMixin
from app.db.models.enums import UserPermissionsEnum


class User(Base, IDMixin, TimestampMixin):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)
    permissions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=lambda: [UserPermissionsEnum.CAN_SELF_DELETE],
        nullable=False,
        server_default=text("'{CAN_SELF_DELETE}'::text[]"),
    )
    use_token_since: Mapped[datetime.datetime] = mapped_column(nullable=True)
