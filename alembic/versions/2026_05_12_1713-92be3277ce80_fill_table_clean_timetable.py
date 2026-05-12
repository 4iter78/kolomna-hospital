"""fill table clean_timetable

Revision ID: 92be3277ce80
Revises: 2d1149c89c47
Create Date: 2026-05-12 17:13:05.492924

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '92be3277ce80'
down_revision: Union[str, Sequence[str], None] = '2d1149c89c47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO clean_timetable (user_id, room_id, clean_datetime) VALUES
    (
        (SELECT id FROM users
         WHERE surname = 'Денисов'
           AND name = 'Антон'
           AND second_name = 'Романович'
           AND employment_date = '2021-02-28'),
        (SELECT id FROM rooms WHERE name = 'Палата №1'),
        '2024-02-01 07:00:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Денисов'
           AND name = 'Антон'
           AND second_name = 'Романович'
           AND employment_date = '2021-02-28'),
        (SELECT id FROM rooms WHERE name = 'Палата №2'),
        '2024-02-01 07:30:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Денисов'
           AND name = 'Антон'
           AND second_name = 'Романович'
           AND employment_date = '2021-02-28'),
        (SELECT id FROM rooms WHERE name = 'Палата №3'),
        '2024-02-01 08:00:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Яковлева'
           AND name = 'Людмила'
           AND second_name = 'Борисовна'
           AND employment_date = '2022-07-15'),
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 1'),
        '2024-02-01 07:00:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Яковлева'
           AND name = 'Людмила'
           AND second_name = 'Борисовна'
           AND employment_date = '2022-07-15'),
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 2'),
        '2024-02-01 07:30:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Денисов'
           AND name = 'Антон'
           AND second_name = 'Романович'
           AND employment_date = '2021-02-28'),
        (SELECT id FROM rooms WHERE name = 'Терапевтический каб. 3'),
        '2024-02-01 08:00:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Яковлева'
           AND name = 'Людмила'
           AND second_name = 'Борисовна'
           AND employment_date = '2022-07-15'),
        (SELECT id FROM rooms WHERE name = 'Процедурная МРТ'),
        '2024-02-01 08:30:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Денисов'
           AND name = 'Антон'
           AND second_name = 'Романович'
           AND employment_date = '2021-02-28'),
        (SELECT id FROM rooms WHERE name = 'Процедурная Рентген'),
        '2024-02-01 09:00:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Яковлева'
           AND name = 'Людмила'
           AND second_name = 'Борисовна'
           AND employment_date = '2022-07-15'),
        (SELECT id FROM rooms WHERE name = 'Процедурная Флюорография'),
        '2024-02-01 09:30:00'
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Денисов'
           AND name = 'Антон'
           AND second_name = 'Романович'
           AND employment_date = '2021-02-28'),
        (SELECT id FROM rooms WHERE name = 'Процедурная №2 МРТ'),
        '2024-02-01 10:00:00'
    );
    ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'Палата №1', '2024-02-01 07:00:00'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'Палата №2', '2024-02-01 07:30:00'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'Палата №3', '2024-02-01 08:00:00'),
        ('Яковлева', 'Людмила', 'Борисовна', '2022-07-15', 'Терапевтический каб. 1', '2024-02-01 07:00:00'),
        ('Яковлева', 'Людмила', 'Борисовна', '2022-07-15', 'Терапевтический каб. 2', '2024-02-01 07:30:00'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'Терапевтический каб. 3', '2024-02-01 08:00:00'),
        ('Яковлева', 'Людмила', 'Борисовна', '2022-07-15', 'Процедурная МРТ', '2024-02-01 08:30:00'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'Процедурная Рентген', '2024-02-01 09:00:00'),
        ('Яковлева', 'Людмила', 'Борисовна', '2022-07-15', 'Процедурная Флюорография', '2024-02-01 09:30:00'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'Процедурная №2 МРТ', '2024-02-01 10:00:00')
    ]

    for surname, name, second_name, employment_date, room_name, clean_datetime in records_to_delete:
        params = {
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'employment_date': employment_date,
            'room_name': room_name,
            'clean_datetime': clean_datetime
        }

        op.get_bind().execute(
            text('''
                DELETE FROM clean_timetable
                WHERE
                    user_id = (
                SELECT id FROM users
                WHERE surname = :surname
                  AND name = :name
                  AND second_name = :second_name
                  AND employment_date = :employment_date
            )
            AND room_id = (SELECT id FROM rooms WHERE name = :room_name)
            AND clean_datetime = :clean_datetime
            '''),
            params
        )
