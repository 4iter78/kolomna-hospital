"""fill table user_roles

Revision ID: 0d5119448b33
Revises: 6e902352114d
Create Date: 2026-06-03 06:36:55.570318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '0d5119448b33'
down_revision: Union[str, Sequence[str], None] = '6e902352114d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO user_roles (name) VALUES
            ('Врач'),
            ('Гость'),
            ('Администратор'),
            ('Провизор'),
            ('Кладовщик'),
            ('Медсестра'),
            ('Фельдшер');
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM user_roles;
    ''')
