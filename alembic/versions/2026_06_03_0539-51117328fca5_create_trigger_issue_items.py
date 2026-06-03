"""create trigger issue_items

Revision ID: 51117328fca5
Revises: 4bb97c43a5b8
Create Date: 2026-06-03 05:39:18.803927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '51117328fca5'
down_revision: Union[str, Sequence[str], None] = '4bb97c43a5b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_issue_item_delete
        AFTER DELETE ON issue_items
        FOR EACH ROW
        EXECUTE FUNCTION trg_issue_items_after_delete();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_issue_item_delete ON issue_items;
    ''')
