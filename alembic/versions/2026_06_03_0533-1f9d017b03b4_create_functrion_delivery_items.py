"""create functrion delivery_items

Revision ID: 1f9d017b03b4
Revises: 062cf0ce927c
Create Date: 2026-06-03 05:33:58.468211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '1f9d017b03b4'
down_revision: Union[str, Sequence[str], None] = '062cf0ce927c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION trg_delivery_items_after_delete()
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
        
            -- Убираем ранее добавленный остаток
            PERFORM update_material_balance(
                OLD.medical_material_id,
                v_storage_department_id,
                -OLD.quantity
            );
        
            RETURN OLD;
        END;
        $$;
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP FUNCTION IF EXISTS trg_delivery_items_after_delete();
    ''')
