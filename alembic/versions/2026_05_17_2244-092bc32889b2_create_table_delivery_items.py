"""create table delivery_items

Revision ID: 092bc32889b2
Revises: 1f7f1fbe84fa
Create Date: 2026-05-17 22:44:13.086562

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '092bc32889b2'
down_revision: Union[str, Sequence[str], None] = '1f7f1fbe84fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE delivery_items (
            id                SERIAL PRIMARY KEY,
            stock_delivery_id INT NOT NULL REFERENCES stock_deliveries(id),
            medical_material_id INT NOT NULL REFERENCES medical_materials(id),
            quantity           INT NOT NULL CHECK (quantity > 0),
            unit_price       DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0)
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS delivery_items;
    ''')
