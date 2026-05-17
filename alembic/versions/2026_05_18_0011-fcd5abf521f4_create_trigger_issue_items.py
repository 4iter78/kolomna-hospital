"""create trigger issue_items

Revision ID: fcd5abf521f4
Revises: d386178e5876
Create Date: 2026-05-18 02:26:44.850998

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fcd5abf521f4'
down_revision: Union[str, Sequence[str], None] = 'd386178e5876'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_issue_item_insert
        AFTER INSERT ON issue_items
        FOR EACH ROW
        EXECUTE FUNCTION trg_issue_items_after_insert();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_issue_item_insert ON issue_items;
    ''')
