"""create table stock_deliveries

Revision ID: 1f7f1fbe84fa
Revises: c72d84fdd30b
Create Date: 2026-05-17 22:42:16.325546

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1f7f1fbe84fa'
down_revision: Union[str, Sequence[str], None] = 'c72d84fdd30b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE stock_deliveries (
            id             SERIAL PRIMARY KEY,
            supplier_id    INT NOT NULL REFERENCES suppliers(id),
            delivery_date DATE NOT NULL,
            document_number VARCHAR(100),  -- номер накладной
            notes         TEXT
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS stock_deliveries;
    ''')
