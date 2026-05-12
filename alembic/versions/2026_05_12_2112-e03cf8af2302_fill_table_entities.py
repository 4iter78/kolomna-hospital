"""fill table entities

Revision ID: e03cf8af2302
Revises: 0bb38347e4f1
Create Date: 2026-05-12 21:12:46.211465

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e03cf8af2302'
down_revision: Union[str, Sequence[str], None] = '0bb38347e4f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO entities (code, name) VALUES
    ('users',            'Пользователи'),
    ('user_roles',       'Роли пользователей'),
    ('patients',         'Пациенты'),
    ('health_cards',     'Медицинские карты'),
    ('work_timetable',   'Расписание работы'),
    ('clean_timetable',  'Расписание уборки'),
    ('diagnosises',      'Диагнозы'),
    ('drugs',            'Препараты'),
    ('treatment_types',  'Типы лечения'),
    ('rooms',            'Помещения'),
    ('room_type',        'Типы помещений')
    ON CONFLICT (code) DO NOTHING;
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM entities
        WHERE code IN (
            'users',
            'user_roles',
            'patients',
            'health_cards',
            'work_timetable',
            'clean_timetable',
            'diagnosises',
            'drugs',
            'treatment_types',
            'rooms',
            'room_type'
        );
    ''')
