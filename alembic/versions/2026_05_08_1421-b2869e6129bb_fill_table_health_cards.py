"""fill table health_cards

Revision ID: b2869e6129bb
Revises: d233e01178d5
Create Date: 2026-05-08 14:21:17.517942

"""
from typing import Sequence, Union, Optional

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'b2869e6129bb'
down_revision: Union[str, Sequence[str], None] = 'd233e01178d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO health_cards (patient_id, create_datetime, user_id) VALUES
    (
        (SELECT id FROM patients
         WHERE surname = 'Иванов'
           AND name = 'Иван'
           AND second_name = 'Иванович'
           AND birth_date = '1980-03-15'),
        '2023-01-10 09:00:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Петрова'
           AND name = 'Мария'
           AND second_name = 'Сергеевна'
           AND birth_date = '1975-07-22'),
        '2023-01-15 10:30:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Сидоров'
           AND name = 'Алексей'
           AND second_name = 'Петрович'
           AND birth_date = '1990-11-01'),
        '2023-02-01 08:45:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Кузнецова'
           AND name = 'Елена'
           AND second_name = 'Владимировна'
           AND birth_date = '1985-05-18'),
        '2023-02-20 11:00:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Новиков'
           AND name = 'Дмитрий'
           AND second_name = 'Андреевич'
           AND birth_date = '1968-09-30'),
        '2023-03-05 09:15:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Морозова'
           AND name = 'Ольга'
           AND second_name = 'Николаевна'
           AND birth_date = '1992-02-14'),
        '2023-03-18 14:00:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Волков'
           AND name = 'Сергей'
           AND second_name = 'Михайлович'
           AND birth_date = '1955-12-05'),
        '2023-04-02 10:00:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Зайцева'
           AND name = 'Наталья'
           AND second_name = 'Юрьевна'
           AND birth_date = '2000-06-25'),
        '2023-04-25 13:30:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Лебедев'
           AND name = 'Андрей'
           AND second_name = 'Олегович'
           AND birth_date = '1978-04-10'),
        '2023-05-10 09:00:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    ),
    (
        (SELECT id FROM patients
         WHERE surname = 'Козлова'
           AND name = 'Татьяна'
           AND second_name = 'Ивановна'
           AND birth_date = '1963-08-19'),
        '2023-05-22 11:45:00',
        (SELECT id FROM users
         WHERE surname = 'Белова'
           AND name = 'Светлана'
           AND second_name = 'Александровна'
           AND employment_date = '2017-01-10')
    );

    ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Иванов', 'Иван', 'Иванович', '1980-03-15', '2023-01-10 09:00:00'),
        ('Петрова', 'Мария', 'Сергеевна', '1975-07-22', '2023-01-15 10:30:00'),
        ('Сидоров', 'Алексей', 'Петрович', '1990-11-01', '2023-02-01 08:45:00'),
        ('Кузнецова', 'Елена', 'Владимировна', '1985-05-18', '2023-02-20 11:00:00'),
        ('Новиков', 'Дмитрий', 'Андреевич', '1968-09-30', '2023-03-05 09:15:00'),
        ('Морозова', 'Ольга', 'Николаевна', '1992-02-14', '2023-03-18 14:00:00'),
        ('Волков', 'Сергей', 'Михайлович', '1955-12-05', '2023-04-02 10:00:00'),
        ('Зайцева', 'Наталья', 'Юрьевна', '2000-06-25', '2023-04-25 13:30:00'),
        ('Лебедев', 'Андрей', 'Олегович', '1978-04-10', '2023-05-10 09:00:00'),
        ('Козлова', 'Татьяна', 'Ивановна', '1963-08-19', '2023-05-22 11:45:00')
    ]

    user_surname, user_name, user_second_name, user_employment_date = 'Белова', 'Светлана', 'Александровна', '2017-01-10'

    for record in records_to_delete:
        surname, name, second_name, birth_date, create_datetime = record

        # Выносим все параметры в отдельный словарь
        params = {
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'birth_date': birth_date,
            'create_datetime': create_datetime
        }

        op.get_bind().execute(
            text('''
            DELETE FROM health_cards
            WHERE patient_id = (
                SELECT id FROM patients
                WHERE surname = :surname
                  AND name = :name
                  AND second_name = :second_name
                  AND birth_date = :birth_date
            )
              AND create_datetime = :create_datetime
            '''), params
        )
