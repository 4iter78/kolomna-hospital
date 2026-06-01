"""create table material_types

Revision ID: c9f2fbf6849a
Revises: b79e80d2b683
Create Date: 2026-05-17 22:34:22.272956

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c9f2fbf6849a'
down_revision: Union[str, Sequence[str], None] = 'b79e80d2b683'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE material_types (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS material_types;
    ''')
