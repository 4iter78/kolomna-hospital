"""create table clean_timetable

Revision ID: 1cdfae18112c
Revises: d4f68ec2b0d7
Create Date: 2026-04-21 12:29:41.802075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cdfae18112c'
down_revision: Union[str, Sequence[str], None] = 'd4f68ec2b0d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE clean_timetable (
            id             SERIAL PRIMARY KEY,
            user_id        INT NOT NULL REFERENCES users (id),
            room_id        INT NOT NULL REFERENCES rooms (id),
            clean_datetime TIMESTAMP NOT NULL
        );
    ''')
    pass



def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS clean_timetable;')
    pass
