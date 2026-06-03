"""create functrion material_operations

Revision ID: e47a06f3b81d
Revises: ce46d24c0112
Create Date: 2026-06-03 05:42:48.436721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'e47a06f3b81d'
down_revision: Union[str, Sequence[str], None] = 'ce46d24c0112'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION trg_material_operations_after_delete()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
            IF OLD.is_issued = TRUE
               OR OLD.is_written_off = TRUE
            THEN
                -- Возвращаем материал обратно
                PERFORM update_material_balance(
                    OLD.medical_material_id,
                    OLD.department_id,
                    OLD.quantity
                );
            END IF;
        
            RETURN OLD;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_material_operations_after_delete();
    ''')
