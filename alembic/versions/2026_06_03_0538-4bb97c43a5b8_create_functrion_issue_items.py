"""create functrion issue_items

Revision ID: 4bb97c43a5b8
Revises: a2b94237b43a
Create Date: 2026-06-03 05:38:22.335801

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4bb97c43a5b8'
down_revision: Union[str, Sequence[str], None] = 'a2b94237b43a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION trg_issue_items_after_delete()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        DECLARE
            v_storage_department_id INT;
            v_target_department_id INT;
        BEGIN
            SELECT id
            INTO v_storage_department_id
            FROM departments
            WHERE name = 'Склад';
        
            SELECT department_id
            INTO v_target_department_id
            FROM material_issues
            WHERE id = OLD.material_issue_id;
        
            -- Возвращаем на склад
            PERFORM update_material_balance(
                OLD.medical_material_id,
                v_storage_department_id,
                OLD.quantity
            );
        
            -- Убираем из отделения
            PERFORM update_material_balance(
                OLD.medical_material_id,
                v_target_department_id,
                -OLD.quantity
            );
        
            RETURN OLD;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_issue_items_after_delete();
    ''')
