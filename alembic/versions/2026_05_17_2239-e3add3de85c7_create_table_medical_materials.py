"""create table medical_materials

Revision ID: e3add3de85c7
Revises: 6fb09a738aab
Create Date: 2026-05-17 22:39:03.168303

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e3add3de85c7'
down_revision: Union[str, Sequence[str], None] = '6fb09a738aab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE medical_materials (
            id              SERIAL PRIMARY KEY,
            name            VARCHAR(255) NOT NULL,
            material_type_id INT NOT NULL REFERENCES material_types(id),
            material_unit_id         INT NOT NULL REFERENCES material_units(id),
            description     TEXT
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS medical_materials;
    ''')
