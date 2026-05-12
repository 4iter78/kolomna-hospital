"""fill table drugs

Revision ID: 52012fb52346
Revises: 6e1eac001b5b
Create Date: 2026-04-21 14:22:40.293610

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '52012fb52346'
down_revision: Union[str, Sequence[str], None] = '6e1eac001b5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO drugs (name) VALUES
            ('Аспирин'),
            ('Амоксициллин'),
            ('Метформин'),
            ('Лизиноприл'),
            ('Омепразол'),
            ('Ибупрофен'),
            ('Цетиризин'),
            ('Аторвастатин'),
            ('Амброксол'),
            ('Диклофенак');
    ''')
    pass

def downgrade() -> None:
    op.execute('''
        DELETE FROM drugs WHERE name IN ('Аспирин',
            'Амоксициллин',
            'Метформин',
            'Лизиноприл',
            'Омепразол',
            'Ибупрофен',
            'Цетиризин',
            'Аторвастатин',
            'Амброксол',
            'Диклофенак');
    ''')
    pass
