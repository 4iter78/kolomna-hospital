"""create table health_cards

Revision ID: 39d49f1db9a1
Revises: 0d8e536836ce
Create Date: 2026-04-21 12:14:48.630316

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '39d49f1db9a1'
down_revision: Union[str, Sequence[str], None] = '0d8e536836ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE health_cards (
            id              SERIAL PRIMARY KEY,
            patient_id      INT NOT NULL REFERENCES patients (id),
            create_datetime TIMESTAMP NOT NULL DEFAULT NOW(),
            user_id         INT NOT NULL REFERENCES users (id)
        );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS health_cards;')
