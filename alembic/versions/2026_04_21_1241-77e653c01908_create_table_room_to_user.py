"""create table room_to_user

Revision ID: 77e653c01908
Revises: 150348675518
Create Date: 2026-04-21 12:41:45.735893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77e653c01908'
down_revision: Union[str, Sequence[str], None] = '150348675518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE room_to_user (
            id      SERIAL PRIMARY KEY,
            room_id INT NOT NULL REFERENCES rooms (id),
            user_id INT NOT NULL REFERENCES users (id)
        );
    ''')
    pass
def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS room_to_user;')
    pass
