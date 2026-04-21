"""create table users

Revision ID: 0d8e536836ce
Revises: 3e60c935910a
Create Date: 2026-04-21 12:09:37.884890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d8e536836ce'
down_revision: Union[str, Sequence[str], None] = '3e60c935910a'
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
    pass

def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS users;')
    pass
