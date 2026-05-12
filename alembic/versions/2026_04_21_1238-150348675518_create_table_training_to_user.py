"""create table training_to_user

Revision ID: 150348675518
Revises: 6494f9f3d84c
Create Date: 2026-04-21 12:38:21.439629

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '150348675518'
down_revision: Union[str, Sequence[str], None] = '6494f9f3d84c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE training_to_user (
            id          SERIAL PRIMARY KEY,
            training_id INT NOT NULL REFERENCES training (id),
            user_id     INT NOT NULL REFERENCES users (id)
        );
    ''')
    pass
def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS training_to_user;')
    pass
