"""create trigger material_operations

Revision ID: 9a0a73d94f41
Revises: e47a06f3b81d
Create Date: 2026-06-03 05:43:27.384664

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9a0a73d94f41'
down_revision: Union[str, Sequence[str], None] = 'e47a06f3b81d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_material_operation_delete
        AFTER DELETE ON material_operations
        FOR EACH ROW
        EXECUTE FUNCTION trg_material_operations_after_delete();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_material_operation_delete ON material_operations;
    ''')
