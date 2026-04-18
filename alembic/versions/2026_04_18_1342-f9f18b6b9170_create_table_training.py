"""create table training

Revision ID: f9f18b6b9170
Revises: 663b9a6068c8
Create Date: 2026-04-18 13:42:41.950673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9f18b6b9170'
down_revision: Union[str, Sequence[str], None] = '663b9a6068c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE training (
            id             SERIAL PRIMARY KEY,
            name           VARCHAR(255) NOT NULL,
            special_type_id INT NOT NULL REFERENCES special_type (id)
        );
    ''')
    pass


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS training;')
    pass

