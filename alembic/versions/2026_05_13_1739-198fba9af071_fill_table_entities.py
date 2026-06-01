"""fill table entities

Revision ID: 198fba9af071
Revises: 60e9ce0211b6
Create Date: 2026-05-13 17:39:29.996098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '198fba9af071'
down_revision: Union[str, Sequence[str], None] = '60e9ce0211b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
       INSERT INTO entities (code, name) VALUES 
       ('appointments', 'Приёмы');
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM entities
        WHERE code = 'appointments';
    ''')
