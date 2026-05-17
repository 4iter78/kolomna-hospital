"""fill table stock_deliveries

Revision ID: e75712ee9497
Revises: 270ef522b016
Create Date: 2026-05-18 00:41:44.450946

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e75712ee9497'
down_revision: Union[str, Sequence[str], None] = '270ef522b016'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO stock_deliveries (
            supplier_id,
            delivery_date,
            document_number,
            notes
        )
        VALUES
            (
                (SELECT id FROM suppliers WHERE name = 'МедСнаб'),
                '2026-04-01',
                'MS-001',
                'Плановая поставка'
            ),
            (
                (SELECT id FROM suppliers WHERE name = 'ФармТорг'),
                '2026-04-10',
                'FT-002',
                'Срочная поставка'
            );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM stock_deliveries
        WHERE supplier_id IN (
            (SELECT id FROM suppliers WHERE name = 'МедСнаб'),
            (SELECT id FROM suppliers WHERE name = 'ФармТорг')
        );
    ''')
