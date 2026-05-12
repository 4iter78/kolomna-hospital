"""create table treatment_types

Revision ID: 1afbee1c0eb1
Revises: 8e0e605d9495
Create Date: 2026-04-16 23:32:31.494088

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1afbee1c0eb1'
down_revision: Union[str, Sequence[str], None] = '8e0e605d9495'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('''
        CREATE TABLE treatment_types (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    ''')
    pass

def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS treatment_types;')
    pass

