"""fill table departments

Revision ID: 4f048a2bf6be
Revises: 18fdc043de0c
Create Date: 2026-05-18 00:24:24.267950

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4f048a2bf6be'
down_revision: Union[str, Sequence[str], None] = '18fdc043de0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO departments (name) VALUES
            ('Приёмное отделение'),
            ('Стационарное отделение'),
            ('Реанимация'),
            ('Скорая'),
            ('Медицинский пункт'),
            ('Травматологический пункт'),
            ('Аптека'),
            ('Склад'),
            ('Ожоговое отделение'),
            ('Кардиологическое отделение'),
            ('Хирургическое отделение'),
            ('Отдел информационных технологий'),
            ('Администрация');
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM departments;
    ''')
