"""fill table work_timetable

Revision ID: 2d1149c89c47
Revises: c42c412e152a
Create Date: 2026-05-12 17:00:02.040353

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '2d1149c89c47'
down_revision: Union[str, Sequence[str], None] = 'c42c412e152a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO work_timetable (room_id, work_date, time_from, time_to) VALUES
    (
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 1'),
        '2024-02-01',
        '08:00',
        '14:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 1'),
        '2024-02-02',
        '08:00',
        '14:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 2'),
        '2024-02-01',
        '14:00',
        '20:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 2'),
        '2024-02-02',
        '14:00',
        '20:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 3'),
        '2024-02-01',
        '08:00',
        '16:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Процедурная МРТ'),
        '2024-02-01',
        '09:00',
        '17:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Процедурная Рентген'),
        '2024-02-01',
        '09:00',
        '17:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Процедурная Флюорография'),
        '2024-02-01',
        '10:00',
        '18:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 3'),
        '2024-02-03',
        '08:00',
        '16:00'
    ),
    (
        (SELECT id FROM rooms WHERE name = 'Процедурная МРТ'),
        '2024-02-03',
        '09:00',
        '17:00'
    );
    ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Терапевтический каб. 1', '2024-02-01', '08:00', '14:00'),
        ('Терапевтический каб. 1', '2024-02-02', '08:00', '14:00'),
        ('Терапевтический каб. 2', '2024-02-01', '14:00', '20:00'),
        ('Терапевтический каб. 2', '2024-02-02', '14:00', '20:00'),
        ('Терапевтический каб. 3', '2024-02-01', '08:00', '16:00'),
        ('Процедурная МРТ', '2024-02-01', '09:00', '17:00'),
        ('Процедурная Рентген', '2024-02-01', '09:00', '17:00'),
        ('Процедурная Флюорография', '2024-02-01', '10:00', '18:00'),
        ('Терапевтический каб. 3', '2024-02-03', '08:00', '16:00'),
        ('Процедурная МРТ', '2024-02-03', '09:00', '17:00')
    ]

    for room_name, work_date, time_from, time_to in records_to_delete:
        params = {
            'room_name': room_name,
            'work_date': work_date,
            'time_from': time_from,
            'time_to': time_to
        }

        op.get_bind().execute(
            text('''
            DELETE FROM work_timetable
            WHERE
                room_id = (SELECT id FROM rooms WHERE name = :room_name)
                AND work_date = :work_date
                AND time_from = :time_from
                AND time_to = :time_to
            '''),
            params
        )
