"""create function delivery_items

Revision ID: a4111768fd2e
Revises: ab528f2f82cb
Create Date: 2026-05-18 02:17:57.747651

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a4111768fd2e'
down_revision: Union[str, Sequence[str], None] = 'ab528f2f82cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        -- =========================================
        -- Поступление материалов на склад
        -- =========================================
        
        CREATE OR REPLACE FUNCTION trg_delivery_items_after_insert()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        DECLARE
            v_storage_department_id INT;
        BEGIN
        
            -- Находим отдел "Склад"
            SELECT id
            INTO v_storage_department_id
            FROM departments
            WHERE name = 'Склад';
        
            -- Увеличиваем остаток
            PERFORM update_material_balance(
                NEW.medical_material_id,
                v_storage_department_id,
                NEW.quantity
            );
        
            RETURN NEW;
        END;
        $$

    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_delivery_items_after_insert();
    ''')
