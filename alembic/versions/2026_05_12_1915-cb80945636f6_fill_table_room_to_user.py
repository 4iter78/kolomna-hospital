"""fill table room_to_user

Revision ID: cb80945636f6
Revises: b89bbcd1db05
Create Date: 2026-05-12 19:15:44.255301

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'cb80945636f6'
down_revision: Union[str, Sequence[str], None] = 'b89bbcd1db05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO room_to_user (room_id, user_id)
VALUES
    ((SELECT id FROM rooms WHERE name = 'Терапевтический каб. 1'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM rooms WHERE name = 'Терапевтический каб. 2'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM rooms WHERE name = 'Терапевтический каб. 3'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM rooms WHERE name = 'Процедурная МРТ'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM rooms WHERE name = 'Процедурная Рентген'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM rooms WHERE name = 'Процедурная Флюорография'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM rooms WHERE name = 'Палата №1'),
     (SELECT id FROM users WHERE surname = 'Денисов' AND name = 'Антон' AND second_name = 'Романович' AND employment_date = '2021-02-28')),
    ((SELECT id FROM rooms WHERE name = 'Палата №2'),
     (SELECT id FROM users WHERE surname = 'Яковлева' AND name = 'Людмила' AND second_name = 'Борисовна' AND employment_date = '2022-07-15')),
    ((SELECT id FROM rooms WHERE name = 'Палата №3'),
     (SELECT id FROM users WHERE surname = 'Денисов' AND name = 'Антон' AND second_name = 'Романович' AND employment_date = '2021-02-28')),
    ((SELECT id FROM rooms WHERE name = 'Процедурная №2 МРТ'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15'));
    ''')


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Терапевтический каб. 1', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Терапевтический каб. 2', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Терапевтический каб. 3', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Процедурная МРТ', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Процедурная Рентген', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Процедурная Флюорография', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Палата №1', 'Денисов', 'Антон', 'Романович', '2021-02-28'),
        ('Палата №2', 'Яковлева', 'Людмила', 'Борисовна', '2022-07-15'),
        ('Палата №3', 'Денисов', 'Антон', 'Романович', '2021-02-28'),
        ('Процедурная №2 МРТ', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15')
    ]

    for record in records_to_delete:
        room_name, surname, name, second_name, employment_date = record

        # Выносим все параметры в отдельный словарь
        params = {
            'room_name': room_name,
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'employment_date': employment_date
        }

        op.get_bind().execute(
            text('''
            DELETE FROM room_to_user
            WHERE room_id = (
                SELECT id FROM rooms
                WHERE name = :room_name
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
