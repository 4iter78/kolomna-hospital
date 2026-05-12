"""create table requests

Revision ID: f8d1c32bbae4
Revises: 121121a9487a
Create Date: 2026-04-21 12:56:24.695589

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f8d1c32bbae4'
down_revision: Union[str, Sequence[str], None] = '121121a9487a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE requests (
            id           SERIAL PRIMARY KEY,
            request_file TEXT
        );
    ''')
    pass


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS requests;')
    pass
