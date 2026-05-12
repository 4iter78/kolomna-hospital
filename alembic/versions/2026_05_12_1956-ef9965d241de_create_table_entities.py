"""create table entities

Revision ID: ef9965d241de
Revises: d97ba21c19b5
Create Date: 2026-05-12 19:56:48.242665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'ef9965d241de'
down_revision: Union[str, Sequence[str], None] = 'd97ba21c19b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE TABLE IF NOT EXISTS entities (
    id   SERIAL PRIMARY KEY,
    code VARCHAR(50)  UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
    );
    ''')
    pass


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS entities;')
