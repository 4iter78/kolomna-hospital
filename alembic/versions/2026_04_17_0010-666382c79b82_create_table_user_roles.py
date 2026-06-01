"""create table user_roles

Revision ID: 666382c79b82
Revises: 70101c54188a
Create Date: 2026-04-17 00:10:21.906115

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '666382c79b82'
down_revision: Union[str, Sequence[str], None] = '70101c54188a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
       CREATE TABLE user_roles (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS user_roles;')
