"""create trigger issue_items

Revision ID: ce46d24c0112
Revises: 02267c7a93cc
Create Date: 2026-06-03 05:41:41.848321

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ce46d24c0112'
down_revision: Union[str, Sequence[str], None] = '02267c7a93cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_issue_item_update
        AFTER UPDATE ON issue_items
        FOR EACH ROW
        EXECUTE FUNCTION trg_issue_items_after_update();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_issue_item_update ON issue_items;
    ''')
