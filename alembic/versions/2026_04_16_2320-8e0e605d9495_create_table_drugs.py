"""create table drugs

Revision ID: 8e0e605d9495
Revises: e30f1b76b007
Create Date: 2026-04-16 23:20:21.960074

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8e0e605d9495'
down_revision: Union[str, Sequence[str], None] = 'e30f1b76b007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE drugs (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
    ''')
    pass

def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS drugs;')
    pass