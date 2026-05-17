"""fill table material_units

Revision ID: aa6a3814abe3
Revises: cd04016f67af
Create Date: 2026-05-18 00:34:02.878944

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'aa6a3814abe3'
down_revision: Union[str, Sequence[str], None] = 'cd04016f67af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO material_units (name, short_name) VALUES
            ('Штука', 'шт'),
            ('Упаковка', 'уп'),
            ('Миллилитр', 'мл'),
            ('Грамм', 'г'),
            ('Пара', 'пар');
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM material_units
        WHERE name IN (
            'Штука',
            'Упаковка',
            'Миллилитр',
            'Грамм',
            'Пара'
        );
    ''')
