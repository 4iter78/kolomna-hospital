"""create function material_operations

Revision ID: df35fed3496e
Revises: fcd5abf521f4
Create Date: 2026-05-18 02:32:13.973867

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'df35fed3496e'
down_revision: Union[str, Sequence[str], None] = 'fcd5abf521f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        -- =========================================
        -- Списание / внешняя выдача
        -- =========================================
        
        CREATE OR REPLACE FUNCTION trg_material_operations_after_insert()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
        
            -- Если операция списания или выдачи
            IF NEW.is_issued = TRUE
               OR NEW.is_written_off = TRUE
            THEN
        
                -- Уменьшаем остаток
                PERFORM update_material_balance(
                    NEW.medical_material_id,
                    NEW.department_id,
                    -NEW.quantity
                );
        
            END IF;
        
            RETURN NEW;
        END;
        $$
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_material_operations_after_insert();
    ''')
