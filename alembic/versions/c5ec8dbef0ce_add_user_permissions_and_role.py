"""add user permissions and role

Revision ID: c5ec8dbef0ce
Revises: 211d8e506f6e
Create Date: 2026-03-22 16:24:48.105227

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5ec8dbef0ce"
down_revision: str | Sequence[str] | None = "211d8e506f6e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.Column(
            "permissions",
            sa.ARRAY(sa.String()),
            server_default=sa.text("'{CAN_SELF_DELETE}'::text[]"),
            nullable=False,
        ),
        sa.Column("use_token_since", sa.DateTime(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
