"""create table users

Revision ID: 0d8e536836ce
Revises: 666382c79b82
Create Date: 2026-04-21 12:09:37.884890

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0d8e536836ce'
down_revision: Union[str, Sequence[str], None] = '666382c79b82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE users (
            id              SERIAL PRIMARY KEY,
            surname         VARCHAR(100) NOT NULL,
            name            VARCHAR(100) NOT NULL,
            second_name     VARCHAR(100),
            employment_date DATE NOT NULL,
            user_role_id    INT NOT NULL REFERENCES user_roles (id)
        );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS users;')
