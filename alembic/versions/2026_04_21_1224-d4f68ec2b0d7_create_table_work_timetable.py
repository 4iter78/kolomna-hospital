"""create table work_timetable

Revision ID: d4f68ec2b0d7
Revises: 6a5b928a5e7b
Create Date: 2026-04-21 12:24:49.422309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4f68ec2b0d7'
down_revision: Union[str, Sequence[str], None] = '6a5b928a5e7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE work_timetable (
            id        SERIAL PRIMARY KEY,
            room_id   INT NOT NULL REFERENCES rooms (id),
            work_date DATE NOT NULL,
            time_from TIME NOT NULL,
            time_to   TIME NOT NULL,
            CONSTRAINT chk_time CHECK (time_to > time_from)
        );
    ''')
    pass


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS work_timetable;')
    pass
