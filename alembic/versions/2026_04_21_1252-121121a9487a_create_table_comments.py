"""create table comments

Revision ID: 121121a9487a
Revises: 48ee59758eb7
Create Date: 2026-04-21 12:52:50.710708

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '121121a9487a'
down_revision: Union[str, Sequence[str], None] = '48ee59758eb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE comments (
            id              SERIAL PRIMARY KEY,
            from_patient_id INT NOT NULL REFERENCES patients (id),
            description     TEXT NOT NULL,
            date            DATE NOT NULL DEFAULT CURRENT_DATE,
            to_user_id      INT NOT NULL REFERENCES users (id)
        );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS comments;')
