"""fill table diagnosises

Revision ID: 6e1eac001b5b
Revises: 564e052139d9
Create Date: 2026-04-21 14:14:02.028881

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6e1eac001b5b'
down_revision: Union[str, Sequence[str], None] = '564e052139d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO diagnosises (name) VALUES
            ('Гипертония'),
            ('Сахарный диабет 2 типа'),
            ('Острый бронхит'),
            ('Пневмония'),
            ('Остеохондроз'),
            ('Гастрит'),
            ('Анемия'),
            ('Артрит'),
            ('Мигрень'),
            ('ОРВИ');
    ''')
    pass

def downgrade() -> None:
    op.execute('''
        DELETE FROM diagnosises WHERE name IN ('Гипертония',
            'Сахарный диабет 2 типа',
            'Острый бронхит',
            'Пневмония',
            'Остеохондроз',
            'Гастрит',
            'Анемия',
            'Артрит',
            'Мигрень',
            'ОРВИ');
    ''')
    pass
