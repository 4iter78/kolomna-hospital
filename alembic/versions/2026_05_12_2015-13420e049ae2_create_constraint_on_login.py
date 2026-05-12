"""create constraint on login

Revision ID: 13420e049ae2
Revises: 7beb1bbe67e7
Create Date: 2026-05-12 20:15:05.818701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '13420e049ae2'
down_revision: Union[str, Sequence[str], None] = '7beb1bbe67e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE users
    ADD CONSTRAINT uq_users_login UNIQUE (login);
    ''')


def downgrade() -> None:
    op.execute('''
    ALTER TABLE users DROP CONSTRAINT uq_users_login;
    ''')
