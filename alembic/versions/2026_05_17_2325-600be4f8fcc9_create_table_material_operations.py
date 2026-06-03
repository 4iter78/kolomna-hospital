"""create table material_operations

Revision ID: 600be4f8fcc9
Revises: 20d213b68207
Create Date: 2026-05-17 23:25:44.815894

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '600be4f8fcc9'
down_revision: Union[str, Sequence[str], None] = '20d213b68207'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE material_operations (
            id SERIAL PRIMARY KEY,
            medical_material_id INT NOT NULL
                REFERENCES medical_materials(id),
            quantity INT NOT NULL
                CHECK (quantity > 0),
            -- чек, акт списания, рецепт, накладная и т.д.
            document_number VARCHAR(100),
            current_user_id INT NOT NULL
                REFERENCES users(id),
            department_id INT NOT NULL REFERENCES departments(id),
            operation_date TIMESTAMP NOT NULL
                DEFAULT NOW(),
            description TEXT,
            -- Флаг выдачи
            is_issued BOOLEAN NOT NULL DEFAULT FALSE,
            -- Флаг списания
            is_written_off BOOLEAN NOT NULL DEFAULT FALSE,
            -- Проверка:
            -- хотя бы один флаг должен быть TRUE
            CONSTRAINT chk_operation_type
            CHECK (
                is_issued = TRUE
                OR
                is_written_off = TRUE
            )
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS material_operations;
    ''')
