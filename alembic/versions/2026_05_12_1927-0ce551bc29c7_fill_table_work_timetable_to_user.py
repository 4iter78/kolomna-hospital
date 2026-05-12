"""fill table work_timetable_to_user

Revision ID: 0ce551bc29c7
Revises: cb80945636f6
Create Date: 2026-05-12 19:27:33.118564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '0ce551bc29c7'
down_revision: Union[str, Sequence[str], None] = 'cb80945636f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO work_timetable_to_user (work_timetable_id, user_id)
VALUES
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 1')
        AND work_date = '2024-02-01'
        AND time_from = '08:00'
        AND time_to = '14:00'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 1')
        AND work_date = '2024-02-02'
        AND time_from = '08:00'
        AND time_to = '14:00'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 2')
        AND work_date = '2024-02-01'
        AND time_from = '14:00'
        AND time_to = '20:00'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 2')
        AND work_date = '2024-02-02'
        AND time_from = '14:00'
        AND time_to = '20:00'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 3')
        AND work_date = '2024-02-01'
        AND time_from = '08:00'
        AND time_to = '16:00'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Процедурная МРТ')
        AND work_date = '2024-02-01'
        AND time_from = '09:00'
        AND time_to = '17:00'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Процедурная Рентген')
        AND work_date = '2024-02-01'
        AND time_from = '09:00'
        AND time_to = '17:00'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Процедурная Флюорография')
        AND work_date = '2024-02-01'
        AND time_from = '10:00'
        AND time_to = '18:00'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 3')
        AND work_date = '2024-02-03'
        AND time_from = '08:00'
        AND time_to = '16:00'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM work_timetable
      WHERE room_id = (SELECT id FROM rooms WHERE name = 'Процедурная МРТ')
        AND work_date = '2024-02-03'
        AND time_from = '09:00'
        AND time_to = '17:00'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01'));
     ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Терапевтический каб. 1', '2024-02-01', '08:00', '14:00', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Терапевтический каб. 1', '2024-02-02', '08:00', '14:00', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Терапевтический каб. 2', '2024-02-01', '14:00', '20:00', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Терапевтический каб. 2', '2024-02-02', '14:00', '20:00', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Терапевтический каб. 3', '2024-02-01', '08:00', '16:00', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Процедурная МРТ', '2024-02-01', '09:00', '17:00', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Процедурная Рентген', '2024-02-01', '09:00', '17:00', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Процедурная Флюорография', '2024-02-01', '10:00', '18:00', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Терапевтический каб. 3', '2024-02-03', '08:00', '16:00', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Процедурная МРТ', '2024-02-03', '09:00', '17:00', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01')
    ]

    for record in records_to_delete:
        room_name, work_date, time_from, time_to, surname, name, second_name, employment_date = record

        # Выносим все параметры в отдельный словарь
        params = {
            'room_name': room_name,
            'work_date': work_date,
            'time_from': time_from,
            'time_to': time_to,
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'employment_date': employment_date
        }

        op.get_bind().execute(
            text('''
            DELETE FROM work_timetable_to_user
            WHERE work_timetable_id = (
                SELECT wt.id FROM work_timetable wt
                JOIN rooms r ON wt.room_id = r.id
                WHERE r.name = :room_name
                  AND wt.work_date = :work_date
                  AND wt.time_from = :time_from
                  AND wt.time_to = :time_to
            )
            AND user_id = (
                SELECT id FROM users
                WHERE surname = :surname
                  AND name = :name
                  AND second_name = :second_name
                  AND employment_date = :employment_date
            )
            '''), params
        )
