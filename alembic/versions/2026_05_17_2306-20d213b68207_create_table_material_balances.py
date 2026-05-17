"""create table material_balances

Revision ID: 20d213b68207
Revises: 017fcffcab19
Create Date: 2026-05-17 23:06:34.982323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '20d213b68207'
down_revision: Union[str, Sequence[str], None] = '017fcffcab19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE material_balances (
            id                 SERIAL PRIMARY KEY,
            medical_material_id INT NOT NULL REFERENCES medical_materials(id),
            current_quantity   INT NOT NULL DEFAULT 0 CHECK (current_quantity >= 0),
            last_updated      TIMESTAMP NOT NULL DEFAULT NOW(),
            department       INT NOT NULL REFERENCES departments(id)
        );
    ''')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS material_balances;
    ''')
    pass
