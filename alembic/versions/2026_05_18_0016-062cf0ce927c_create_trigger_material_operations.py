"""create trigger material_operations

Revision ID: 062cf0ce927c
Revises: df35fed3496e
Create Date: 2026-05-18 02:33:57.956070

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '062cf0ce927c'
down_revision: Union[str, Sequence[str], None] = 'df35fed3496e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TRIGGER after_material_operation_insert
        AFTER INSERT ON material_operations
        FOR EACH ROW
        EXECUTE FUNCTION trg_material_operations_after_insert();
    ''')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TRIGGER IF EXISTS after_material_operation_insert ON material_operations;
    ''')
    pass
