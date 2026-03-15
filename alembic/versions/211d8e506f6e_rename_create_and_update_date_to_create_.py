"""rename create and update date to create and update at

Revision ID: 211d8e506f6e
Revises: 9acd0cc97a65
Create Date: 2026-03-15 17:23:34.019875

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "211d8e506f6e"
down_revision: str | Sequence[str] | None = "9acd0cc97a65"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("companies", "created_date", new_column_name="created_at")
    op.alter_column("companies", "updated_date", new_column_name="updated_at")
    op.alter_column("items", "created_date", new_column_name="created_at")
    op.alter_column("items", "updated_date", new_column_name="updated_at")


def downgrade() -> None:
    op.alter_column("companies", "created_at", new_column_name="created_date")
    op.alter_column("companies", "updated_at", new_column_name="updated_date")
    op.alter_column("items", "created_at", new_column_name="created_date")
    op.alter_column("items", "updated_at", new_column_name="updated_date")
