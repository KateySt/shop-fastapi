"""add price and currency for item

Revision ID: 9acd0cc97a65
Revises: c047e2e6163b
Create Date: 2026-03-08 14:08:46.787824

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9acd0cc97a65'
down_revision: Union[str, Sequence[str], None] = 'c047e2e6163b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    currency_enum = sa.Enum('UAH', 'USD', 'EUR', name='currency_enum')
    currency_enum.create(op.get_bind())

    op.add_column('items',
                  sa.Column(
                      'price',
                      sa.Numeric(precision=10, scale=2),
                      nullable=False,
                      server_default='0.00',
                  )
                  )
    op.add_column('items',
                  sa.Column(
                      'currency',
                      currency_enum,
                      nullable=False,
                      server_default='UAH',
                  )
                  )


def downgrade() -> None:
    op.drop_column('items', 'currency')
    op.drop_column('items', 'price')
