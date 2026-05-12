"""create table room_type

Revision ID: f7533eca5af3
Revises: 604b392359df
Create Date: 2026-04-18 12:53:25.654281

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f7533eca5af3'
down_revision: Union[str, Sequence[str], None] = '604b392359df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE room_type (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    ''')
    pass
def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS room_type;')
    pass
