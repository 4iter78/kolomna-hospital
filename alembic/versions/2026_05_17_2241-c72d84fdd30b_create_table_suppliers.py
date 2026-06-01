"""create table suppliers

Revision ID: c72d84fdd30b
Revises: e3add3de85c7
Create Date: 2026-05-17 22:41:05.399996

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c72d84fdd30b'
down_revision: Union[str, Sequence[str], None] = 'e3add3de85c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE suppliers (
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(255) NOT NULL,
            contact_person VARCHAR(255),
            phone       VARCHAR(20),
            email       VARCHAR(150),
            address     TEXT
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS suppliers;
    ''')
    pass
