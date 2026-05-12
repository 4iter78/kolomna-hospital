"""change table users

Revision ID: 7beb1bbe67e7
Revises: 8880a4462cba
Create Date: 2026-05-12 20:12:47.327126

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7beb1bbe67e7'
down_revision: Union[str, Sequence[str], None] = '8880a4462cba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE users
        ADD COLUMN IF NOT EXISTS login VARCHAR(100),
        ADD COLUMN IF NOT EXISTS password VARCHAR(255),
        ADD COLUMN IF NOT EXISTS hash_password VARCHAR(64);
    ''')


def downgrade() -> None:
    op.execute('''
    ALTER TABLE users
        DROP COLUMN IF EXISTS login,
        DROP COLUMN IF EXISTS password,
        DROP COLUMN IF EXISTS hash_password;
    ''')
