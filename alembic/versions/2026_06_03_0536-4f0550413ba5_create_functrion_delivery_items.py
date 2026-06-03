"""create functrion delivery_items

Revision ID: 4f0550413ba5
Revises: ed5d4f09fc2d
Create Date: 2026-06-03 05:36:15.206228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '4f0550413ba5'
down_revision: Union[str, Sequence[str], None] = 'ed5d4f09fc2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION trg_delivery_items_after_update()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        DECLARE
            v_storage_department_id INT;
        BEGIN
            SELECT id
            INTO v_storage_department_id
            FROM departments
            WHERE name = 'Склад';
        
            -- Отменяем старое поступление
            PERFORM update_material_balance(
                OLD.medical_material_id,
                v_storage_department_id,
                -OLD.quantity
            );
        
            -- Применяем новое
            PERFORM update_material_balance(
                NEW.medical_material_id,
                v_storage_department_id,
                NEW.quantity
            );
        
            RETURN NEW;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_delivery_items_after_update();
    ''')
