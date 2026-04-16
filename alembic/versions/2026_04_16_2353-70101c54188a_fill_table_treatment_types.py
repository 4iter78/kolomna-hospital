"""fill table treatment_types

Revision ID: 70101c54188a
Revises: 1afbee1c0eb1
Create Date: 2026-04-16 23:53:10.244057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70101c54188a'
down_revision: Union[str, Sequence[str], None] = '1afbee1c0eb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO treatment_types (name) VALUES
            ('Амбулаторно'),
            ('Стационар'),
            ('Дневной стационар'),
            ('Госпитализация');
    ''')
    pass

def downgrade() -> None:
    op.execute('''
        DELETE FROM treatment_types WHERE name IN ('Амбулаторно',
            'Стационар',
            'Дневной стационар',
            'Госпитализация');
    ''')
    pass
