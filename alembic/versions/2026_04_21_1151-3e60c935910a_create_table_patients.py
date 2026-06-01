"""create table patients

Revision ID: 3e60c935910a
Revises: f0738fbff61b
Create Date: 2026-04-21 11:51:33.058050

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3e60c935910a'
down_revision: Union[str, Sequence[str], None] = 'f0738fbff61b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE patients (
            id           SERIAL PRIMARY KEY,
            surname      VARCHAR(100) NOT NULL,
            name         VARCHAR(100) NOT NULL,
            second_name  VARCHAR(100),
            birth_date   DATE NOT NULL,
            birth_place  VARCHAR(255),
            phone        VARCHAR(20),
            email        VARCHAR(150),
            address      TEXT,
            passport     VARCHAR(20),
            oms_number   VARCHAR(20)
        );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS patients;')
