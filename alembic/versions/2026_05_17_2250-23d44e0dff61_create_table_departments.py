"""create table departments

Revision ID: 23d44e0dff61
Revises: 092bc32889b2
Create Date: 2026-05-17 22:50:00.284185

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '23d44e0dff61'
down_revision: Union[str, Sequence[str], None] = '092bc32889b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS departments;
    ''')
