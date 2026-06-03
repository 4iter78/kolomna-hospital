"""fill table entities

Revision ID: 6e902352114d
Revises: cd5f63974818
Create Date: 2026-06-03 06:12:50.043167

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6e902352114d'
down_revision: Union[str, Sequence[str], None] = 'cd5f63974818'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO entities (code, name) VALUES
    ('users',            'Пользователи'),
    ('user_roles',       'Роли пользователей'),
    ('suppliers',        'Поставщики'),
    ('delivery',         'Поступление медицинских материалов на склад'),
    ('issue',            'Выдача медицинских материалов'),
    ('storage',          'Хранение медицинских материалов'),
    ('issued',           'Выданные медицинские материалы'),
    ('written_off',      'Списанные медицинские материалы'),
    ('departments',      'Отделения'),
    ('material_types',   'Типы медицинских материалов'),
    ('material_units',   'Единицы измерения материалов')
    ON CONFLICT (code) DO NOTHING;
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM entities
        WHERE code IN (
            'users',
            'user_roles',
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
