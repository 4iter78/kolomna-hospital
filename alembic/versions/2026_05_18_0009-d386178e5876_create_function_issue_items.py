"""create function issue_items

Revision ID: d386178e5876
Revises: 1c0f6842f315
Create Date: 2026-05-18 02:24:32.444323

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd386178e5876'
down_revision: Union[str, Sequence[str], None] = '1c0f6842f315'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        -- =========================================
        -- Выдача материалов в отделение
        -- =========================================
        
        CREATE OR REPLACE FUNCTION trg_issue_items_after_insert()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        DECLARE
            v_storage_department_id INT;
            v_target_department_id INT;
        BEGIN
        
            -- Склад
            SELECT id
            INTO v_storage_department_id
            FROM departments
            WHERE name = 'Склад';
        
            -- Отделение назначения
            SELECT department_id
            INTO v_target_department_id
            FROM material_issues
            WHERE id = NEW.material_issue_id;
        
            -- Уменьшаем остаток склада
            PERFORM update_material_balance(
                NEW.medical_material_id,
                v_storage_department_id,
                -NEW.quantity
            );
        
            -- Увеличиваем остаток отделения
            PERFORM update_material_balance(
                NEW.medical_material_id,
                v_target_department_id,
                NEW.quantity
            );
        
            RETURN NEW;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_issue_items_after_insert();
    ''')
