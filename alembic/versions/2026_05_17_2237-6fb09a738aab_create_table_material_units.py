"""create table material_units

Revision ID: 6fb09a738aab
Revises: c9f2fbf6849a
Create Date: 2026-05-17 22:37:12.810573

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6fb09a738aab'
down_revision: Union[str, Sequence[str], None] = 'c9f2fbf6849a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE material_units (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,  -- шт., упаковка, мл, г и т. д.
            short_name VARCHAR(20) NOT NULL  -- шт, уп, мл, г
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS material_units;
    ''')
