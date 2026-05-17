"""create table department_to_user

Revision ID: 8f2cef6ade51
Revises: 23d44e0dff61
Create Date: 2026-05-17 22:51:58.038099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '8f2cef6ade51'
down_revision: Union[str, Sequence[str], None] = '23d44e0dff61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE department_to_user (
            id SERIAL PRIMARY KEY,
            department_id INT NOT NULL REFERENCES departments (id),
            user_id INT NOT NULL REFERENCES users (id)
        );
    ''')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS department_to_user;
    ''')
    pass
