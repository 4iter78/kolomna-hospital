"""fill table user_roles

Revision ID: 604b392359df
Revises: 666382c79b82
Create Date: 2026-04-17 00:16:10.879202

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '604b392359df'
down_revision: Union[str, Sequence[str], None] = '666382c79b82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO user_roles (name) VALUES
            ('Врач'),
            ('Регистратор'),
            ('Работник ИТ'),
            ('Аспирант'),
            ('Обслуживающий персонал'),
            ('Гость'),
            ('Администратор');
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM user_roles WHERE name IN ('Врач',
            'Регистратор',
            'Работник ИТ',
            'Аспирант',
            'Обслуживающий персонал',
            'Гость',
            'Администратор');
    ''')
