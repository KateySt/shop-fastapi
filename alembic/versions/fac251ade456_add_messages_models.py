"""add messages models

Revision ID: fac251ade456
Revises: 1b9d1bee7fa4
Create Date: 2026-05-03 10:16:13.567732

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fac251ade456"
down_revision: str | Sequence[str] | None = "1b9d1bee7fa4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "messages",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("room", sa.String(), nullable=True),
        sa.Column("channel", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("messages")
