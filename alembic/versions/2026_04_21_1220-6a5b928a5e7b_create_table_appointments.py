"""create table appointments

Revision ID: 6a5b928a5e7b
Revises: 39d49f1db9a1
Create Date: 2026-04-21 12:20:53.115936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5b928a5e7b'
down_revision: Union[str, Sequence[str], None] = '39d49f1db9a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE appointments (
            id                   SERIAL PRIMARY KEY,
            user_id              INT NOT NULL REFERENCES users (id),
            health_card_id       INT NOT NULL REFERENCES health_cards (id),
            treatment_type_id    INT NOT NULL REFERENCES treatment_types (id),
            appointment_datetime TIMESTAMP NOT NULL,
            diagnosis_id         INT REFERENCES diagnosises (id)
        );
    ''')
    pass


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS appointments;')
    pass
