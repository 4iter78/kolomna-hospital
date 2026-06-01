"""fill table rooms

Revision ID: 2e13685d0c97
Revises: 67b709eb8926
Create Date: 2026-04-26 17:14:24.383325

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2e13685d0c97'
down_revision: Union[str, Sequence[str], None] = '67b709eb8926'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
       INSERT INTO rooms (name, room_type_id, special_type_id) VALUES
            ('Палата №1',(SELECT id FROM room_type WHERE name ='Общее'), NULL),
            ('Палата №2',(SELECT id FROM room_type WHERE name ='Общее'), NULL),
            ('Палата №3',(SELECT id FROM room_type WHERE name ='Общее'), NULL),
            ('Терапевтический каб. 1',(SELECT id FROM room_type WHERE name ='Терапевтический кабинет'), NULL),
            ('Терапевтический каб. 2', (SELECT id FROM room_type WHERE name ='Терапевтический кабинет'), NULL),
            ('Терапевтический каб. 3', (SELECT id FROM room_type WHERE name ='Терапевтический кабинет'), NULL),
            ('Процедурная МРТ',(SELECT id FROM room_type WHERE name ='Процедурная'), 
            (SELECT id FROM special_type WHERE name ='МРТ')),
            ('Процедурная Рентген',(SELECT id FROM room_type WHERE name ='Процедурная'), 
            (SELECT id FROM special_type WHERE name ='Рентген')),
            ('Процедурная Флюорография',(SELECT id FROM room_type WHERE name ='Процедурная'), 
            (SELECT id FROM special_type WHERE name ='Флюорография')),
            ('Процедурная №2 МРТ',(SELECT id FROM room_type WHERE name ='Процедурная'), 
            (SELECT id FROM special_type WHERE name ='МРТ'));
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM rooms WHERE name IN ('Палата №1',
            'Палата №2',
            'Палата №3',
            'Терапевтический каб. 1',
            'Терапевтический каб. 2',
            'Терапевтический каб. 3',
            'Процедурная МРТ',
            'Процедурная Рентген',
            'Процедурная Флюорография',
            'Процедурная №2 МРТ');
    ''')
