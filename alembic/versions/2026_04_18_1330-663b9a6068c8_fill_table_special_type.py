"""fill table special_type

Revision ID: 663b9a6068c8
Revises: af25a62c983a
Create Date: 2026-04-18 13:30:26.644675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '663b9a6068c8'
down_revision: Union[str, Sequence[str], None] = 'af25a62c983a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO special_type (name) VALUES
            ('МРТ'),
            ('Рентген'),
            ('Флюорография');
    ''')
    pass
def downgrade() -> None:
    op.execute('''
        DELETE FROM special_type WHERE name IN ('МРТ',
        'Рентген',
        'Флюорография';
    ''')