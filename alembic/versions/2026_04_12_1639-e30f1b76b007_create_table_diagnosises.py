"""create table diagnosises

Revision ID: e30f1b76b007
Revises: 
Create Date: 2026-04-12 16:39:47.535390

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e30f1b76b007'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE diagnosises (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE
        );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS diagnosises;')
