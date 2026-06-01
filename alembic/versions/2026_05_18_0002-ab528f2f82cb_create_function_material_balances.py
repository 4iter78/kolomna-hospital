"""create function material_balances

Revision ID: ab528f2f82cb
Revises: 600be4f8fcc9
Create Date: 2026-05-18 02:09:01.184341

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ab528f2f82cb'
down_revision: Union[str, Sequence[str], None] = '600be4f8fcc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        -- =========================================
        -- Функция изменения остатков
        -- =========================================

        CREATE OR REPLACE FUNCTION update_material_balance(
            p_material_id INT,
            p_department_id INT,
            p_delta INT
        )
        RETURNS VOID
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
        
            -- Если запись уже существует
            UPDATE material_balances
            SET
                current_quantity = current_quantity + p_delta,
                last_updated = NOW()
            WHERE
                medical_material_id = p_material_id
                AND department_id = p_department_id;
        
            -- Если записи нет — создаем
            IF NOT FOUND THEN
        
                INSERT INTO material_balances (
                    medical_material_id,
                    department_id,
                    current_quantity,
                    last_updated
                )
                VALUES (
                    p_material_id,
                    p_department_id,
                    p_delta,
                    NOW()
                );
        
            END IF;
        
        END;
        $$
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS update_material_balance();
    ''')
