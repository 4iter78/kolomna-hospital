"""fill new fields users

Revision ID: 0bb38347e4f1
Revises: 354924229524
Create Date: 2026-05-12 20:28:52.762799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '0bb38347e4f1'
down_revision: Union[str, Sequence[str], None] = '354924229524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    UPDATE users
    SET
        login = data.login,
        password = data.password
    FROM (VALUES
        ('Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'smirnov_pe', 'secret_1'),
        ('Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'fedorova_ad', 'secret_2'),
        ('Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'orlov_ns', 'secret_3'),
        ('Белова', 'Светлана', 'Александровна', '2017-01-10', 'belova_sa', 'secret_4'),
        ('Тихонов', 'Игорь', 'Васильевич', '2019-05-20', 'tikhonov_iv', 'secret_5'),
        ('Громова', 'Ирина', 'Петровна', '2016-11-01', 'gromova_ip', 'secret_6'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28', 'denisov_ar', 'secret_7'),
        ('Яковлева', 'Людмила', 'Борисовна', '2022-07-15', 'yakovleva_lb', 'secret_8'),
        ('Захаров', 'Виктор', 'Геннадьевич', '2014-04-01', 'zakharov_vg', 'secret_9'),
        ('Полякова', 'Кристина', 'Олеговна', '2023-01-09', 'polyakova_ko', 'secret_10')
    ) AS data(surname, name, second_name, employment_date, login, password)
    WHERE users.surname = data.surname
      AND users.name = data.name
      AND users.second_name = data.second_name
      AND users.employment_date = CAST(data.employment_date AS DATE);
    ''')


def downgrade() -> None:
    users_to_null = [
        ('Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Белова', 'Светлана', 'Александровна', '2017-01-10'),
        ('Тихонов', 'Игорь', 'Васильевич', '2019-05-20'),
        ('Громова', 'Ирина', 'Петровна', '2016-11-01'),
        ('Денисов', 'Антон', 'Романович', '2021-02-28'),
        ('Яковлева', 'Людмила', 'Борисовна', '2022-07-15'),
        ('Захаров', 'Виктор', 'Геннадьевич', '2014-04-01'),
        ('Полякова', 'Кристина', 'Олеговна', '2023-01-09')
    ]

    for user in users_to_null:
        (surname, name, second_name, employment_date) = user

        params = {
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'employment_date': employment_date
        }
        op.get_bind().execute(text('''
            UPDATE users
            SET
                login = NULL,
                password = NULL,
                hash_password = NULL
            WHERE surname = :surname
              AND name = :name
              AND second_name = :second_name
              AND employment_date = :employment_date
        '''), params)
