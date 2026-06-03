"""create trigger delivery_items

Revision ID: a2b94237b43a
Revises: 4f0550413ba5
Create Date: 2026-06-03 05:36:51.180285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'a2b94237b43a'
down_revision: Union[str, Sequence[str], None] = '4f0550413ba5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_delivery_item_update
        AFTER UPDATE ON delivery_items
        FOR EACH ROW
        EXECUTE FUNCTION trg_delivery_items_after_update();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_delivery_item_update ON delivery_items;
    ''')
