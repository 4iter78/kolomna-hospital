"""create trigger delivery_items

Revision ID: ed5d4f09fc2d
Revises: 1f9d017b03b4
Create Date: 2026-06-03 05:34:51.099928

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ed5d4f09fc2d'
down_revision: Union[str, Sequence[str], None] = '1f9d017b03b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_delivery_item_delete
        AFTER DELETE ON delivery_items
        FOR EACH ROW
        EXECUTE FUNCTION trg_delivery_items_after_delete();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_delivery_item_delete ON delivery_items;
    ''')
