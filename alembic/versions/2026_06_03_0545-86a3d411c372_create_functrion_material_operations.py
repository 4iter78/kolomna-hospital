"""create functrion material_operations

Revision ID: 86a3d411c372
Revises: 9a0a73d94f41
Create Date: 2026-06-03 05:45:50.780134

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '86a3d411c372'
down_revision: Union[str, Sequence[str], None] = '9a0a73d94f41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION trg_material_operations_after_update()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
            -- Отменяем старое действие
        
            IF OLD.is_issued = TRUE
               OR OLD.is_written_off = TRUE
            THEN
                PERFORM update_material_balance(
                    OLD.medical_material_id,
                    OLD.department_id,
                    OLD.quantity
                );
            END IF;
        
            -- Применяем новое действие
        
            IF NEW.is_issued = TRUE
               OR NEW.is_written_off = TRUE
            THEN
                PERFORM update_material_balance(
                    NEW.medical_material_id,
                    NEW.department_id,
                    -NEW.quantity
                );
            END IF;
        
            RETURN NEW;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_material_operations_after_update();
    ''')
