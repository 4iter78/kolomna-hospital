"""create trigger material_operations

Revision ID: d78f2970ccdd
Revises: 86a3d411c372
Create Date: 2026-06-03 05:46:33.128306

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd78f2970ccdd'
down_revision: Union[str, Sequence[str], None] = '86a3d411c372'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_material_operation_update
        AFTER UPDATE ON material_operations
        FOR EACH ROW
        EXECUTE FUNCTION trg_material_operations_after_update();
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_material_operation_update ON material_operations;
    ''')
