"""create table request_to_user

Revision ID: 564e052139d9
Revises: f8d1c32bbae4
Create Date: 2026-04-21 12:59:03.191521

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '564e052139d9'
down_revision: Union[str, Sequence[str], None] = 'f8d1c32bbae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE request_to_user (
            id         SERIAL PRIMARY KEY,
            request_id INT NOT NULL REFERENCES requests (id),
            user_id    INT NOT NULL REFERENCES users (id)
        );
    ''')
    pass
def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS request_to_user;')
    pass
