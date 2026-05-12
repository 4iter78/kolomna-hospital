"""create table drugs_to_appointment

Revision ID: 6494f9f3d84c
Revises: 1cdfae18112c
Create Date: 2026-04-21 12:34:53.210959

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6494f9f3d84c'
down_revision: Union[str, Sequence[str], None] = '1cdfae18112c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE drugs_to_appointment (
            id             SERIAL PRIMARY KEY,
            drug_id        INT NOT NULL REFERENCES drugs (id),
            appointment_id INT NOT NULL REFERENCES appointments (id)
        );
    ''')
    pass
def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS drugs_to_appointment;')
    pass
