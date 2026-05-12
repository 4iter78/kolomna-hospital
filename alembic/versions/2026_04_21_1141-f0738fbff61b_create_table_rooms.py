"""create table rooms

Revision ID: f0738fbff61b
Revises: f9f18b6b9170
Create Date: 2026-04-21 11:41:12.664492

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f0738fbff61b'
down_revision: Union[str, Sequence[str], None] = 'f9f18b6b9170'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE rooms (
            id              SERIAL PRIMARY KEY,
            name            VARCHAR(255) NOT NULL,
            room_type_id    INT NOT NULL REFERENCES room_type (id),
            special_type_id INT REFERENCES special_type (id),
            CONSTRAINT chk_special_type CHECK (
            special_type_id IS NULL
            OR room_type_id = 3
            )
        );
    ''')
    pass

def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS rooms;')
    pass
