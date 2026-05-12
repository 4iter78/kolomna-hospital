"""create table special_type

Revision ID: af25a62c983a
Revises: 2bd36d738348
Create Date: 2026-04-18 13:17:24.953667

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'af25a62c983a'
down_revision: Union[str, Sequence[str], None] = '2bd36d738348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE special_type (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    ''')
    pass

def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS special_type;')
    pass
