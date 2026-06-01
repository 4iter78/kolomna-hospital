"""create extension pgcrypto

Revision ID: f9fb52931c5e
Revises: 13420e049ae2
Create Date: 2026-05-12 20:12:47.327126

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f9fb52931c5e'
down_revision: Union[str, Sequence[str], None] = '13420e049ae2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    ''')


def downgrade() -> None:
    op.execute('''
    DROP EXTENSION IF EXISTS pgcrypto CASCADE;
    ''')
