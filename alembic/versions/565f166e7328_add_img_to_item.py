"""add img to item

Revision ID: 565f166e7328
Revises: c5ec8dbef0ce
Create Date: 2026-04-05 12:13:22.694751

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "565f166e7328"
down_revision: str | Sequence[str] | None = "c5ec8dbef0ce"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    op.add_column(
        "items",
        sa.Column(
            "images",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{}",
        ),
    )


def downgrade() -> None:
    op.drop_column("items", "images")
