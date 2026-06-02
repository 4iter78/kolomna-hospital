"""fill table entities

Revision ID: efd60a1f2c25
Revises: 7484fc719acd
Create Date: 2026-05-18 04:30:19.842590

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'efd60a1f2c25'
down_revision: Union[str, Sequence[str], None] = '7484fc719acd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO entities (code, name) VALUES
            ('suppliers',        'Поставщики'),
            ('delivery',         'Поступление медицинских материалов на склад'),
            ('issue',            'Выдача медицинских материалов'),
            ('storage',          'Хранение медицинских материалов'),
            ('issued',           'Выданные медицинские материалы'),
            ('written_off',      'Списанные медицинские материалы'),
            ('departments',      'Отделения'),
            ('material_types',   'Типы медицинских материалов'),
            ('material_units',   'Единицы измерения материалов');
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM entities
        WHERE code IN (
            'suppliers',
            'delivery',
            'issue',
            'storage',
            'issued',
            'written_off',
            'departments',
            'material_types',
            'material_units'
        );
    ''')
