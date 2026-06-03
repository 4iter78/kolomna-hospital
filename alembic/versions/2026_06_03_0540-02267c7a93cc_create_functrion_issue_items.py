"""create functrion issue_items

Revision ID: 02267c7a93cc
Revises: 51117328fca5
Create Date: 2026-06-03 05:40:38.560577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '02267c7a93cc'
down_revision: Union[str, Sequence[str], None] = '51117328fca5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION trg_issue_items_after_update()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        DECLARE
            v_storage_department_id INT;
            v_old_department_id INT;
            v_new_department_id INT;
        BEGIN
            SELECT id
            INTO v_storage_department_id
            FROM departments
            WHERE name = 'Склад';
        
            SELECT department_id
            INTO v_old_department_id
            FROM material_issues
            WHERE id = OLD.material_issue_id;
        
            SELECT department_id
            INTO v_new_department_id
            FROM material_issues
            WHERE id = NEW.material_issue_id;
        
            -- Отмена старой выдачи
        
            PERFORM update_material_balance(
                OLD.medical_material_id,
                v_storage_department_id,
                OLD.quantity
            );
        
            PERFORM update_material_balance(
                OLD.medical_material_id,
                v_old_department_id,
                -OLD.quantity
            );
        
            -- Применение новой выдачи
        
            PERFORM update_material_balance(
                NEW.medical_material_id,
                v_storage_department_id,
                -NEW.quantity
            );
        
            PERFORM update_material_balance(
                NEW.medical_material_id,
                v_new_department_id,
                NEW.quantity
            );
        
            RETURN NEW;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_issue_items_after_update();
    ''')
