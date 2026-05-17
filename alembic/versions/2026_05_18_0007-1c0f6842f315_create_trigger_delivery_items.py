"""create trigger delivery_items

Revision ID: 1c0f6842f315
Revises: a4111768fd2e
Create Date: 2026-05-18 02:21:51.637980

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1c0f6842f315'
down_revision: Union[str, Sequence[str], None] = 'a4111768fd2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_delivery_item_insert
        AFTER INSERT ON delivery_items
        FOR EACH ROW
        EXECUTE FUNCTION trg_delivery_items_after_insert();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_delivery_item_insert ON delivery_items;
    ''')
