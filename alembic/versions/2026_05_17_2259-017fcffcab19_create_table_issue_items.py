"""create table issue_items

Revision ID: 017fcffcab19
Revises: 850af15b8073
Create Date: 2026-05-17 22:59:33.969364

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '017fcffcab19'
down_revision: Union[str, Sequence[str], None] = '850af15b8073'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE issue_items (
            id               SERIAL PRIMARY KEY,
            material_issue_id INT NOT NULL REFERENCES material_issues(id),
            medical_material_id INT NOT NULL REFERENCES medical_materials(id),
            quantity         INT NOT NULL CHECK (quantity > 0)
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS issue_items;
    ''')
