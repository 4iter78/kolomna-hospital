"""fill table room_type

Revision ID: 2bd36d738348
Revises: f7533eca5af3
Create Date: 2026-04-18 13:02:55.229965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bd36d738348'
down_revision: Union[str, Sequence[str], None] = 'f7533eca5af3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO room_type (name) VALUES
            ('Общее'),
            ('Терапевтический кабинет'),
            ('Процедурная');
    ''')
    pass

def downgrade() -> None:
    op.execute('''
        DELETE FROM room_type WHERE name IN ('Общее',
            'Терапевтический кабинет',
            'Процедурная');
    ''')
