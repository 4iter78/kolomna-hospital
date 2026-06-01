"""clear table material_balances

Revision ID: 7484fc719acd
Revises: 4c7e01c83cf1
Create Date: 2026-05-18 03:09:21.588785

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7484fc719acd'
down_revision: Union[str, Sequence[str], None] = '4c7e01c83cf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM material_balances;
    ''')
