"""create table work_timetable_to_user

Revision ID: 48ee59758eb7
Revises: 77e653c01908
Create Date: 2026-04-21 12:48:04.311051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48ee59758eb7'
down_revision: Union[str, Sequence[str], None] = '77e653c01908'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE work_timetable_to_user (
            id                SERIAL PRIMARY KEY,
            work_timetable_id INT NOT NULL REFERENCES work_timetable (id),
            user_id           INT NOT NULL REFERENCES users (id)
        );
    ''')
    pass


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS work_timetable_to_user;')
    pass
