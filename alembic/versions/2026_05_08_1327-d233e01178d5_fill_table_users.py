"""fill table users

Revision ID: d233e01178d5
Revises: a44af84a2daa
Create Date: 2026-05-08 13:27:15.048800

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'd233e01178d5'
down_revision: Union[str, Sequence[str], None] = 'a44af84a2daa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
       INSERT INTO users (surname, name, second_name, employment_date, user_role_id) VALUES
            ('Смирнов',    'Павел',      'Евгеньевич',  '2015-06-01', (SELECT id FROM user_roles WHERE name ='Врач')),  -- Врач
            ('Федорова',   'Анна',       'Дмитриевна',  '2018-03-15', (SELECT id FROM user_roles WHERE name ='Врач')),  -- Врач
            ('Орлов',      'Николай',    'Сергеевич',   '2020-09-01', (SELECT id FROM user_roles WHERE name ='Врач')),  -- Врач
            ('Белова',     'Светлана',   'Александровна','2017-01-10', (SELECT id FROM user_roles WHERE name ='Регистратор')), -- Регистратор
            ('Тихонов',    'Игорь',      'Васильевич',  '2019-05-20', (SELECT id FROM user_roles WHERE name ='Работник ИТ')),  -- Работник ИТ
            ('Громова',    'Ирина',      'Петровна',    '2016-11-01', (SELECT id FROM user_roles WHERE name ='Аспирант')),  -- Аспирант
            ('Денисов',    'Антон',      'Романович',   '2021-02-28', (SELECT id FROM user_roles WHERE name ='Обслуживающий персонал')),  -- Обслуживающий персонал
            ('Яковлева',   'Людмила',    'Борисовна',   '2022-07-15', (SELECT id FROM user_roles WHERE name ='Обслуживающий персонал')),  -- Обслуживающий персонал
            ('Захаров',    'Виктор',     'Геннадьевич', '2014-04-01', (SELECT id FROM user_roles WHERE name ='Администратор')),  -- Администратор
            ('Полякова',   'Кристина',   'Олеговна',    '2023-01-09', (SELECT id FROM user_roles WHERE name ='Гость'));  -- Гость

    ''')
    pass


def downgrade() -> None:
    users_to_delete = [
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

    for user in users_to_delete:
        (surname, name, second_name, employment_date) = user

        # Формируем словарь параметров для именованных плейсхолдеров
        params = {
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'employment_date': employment_date
        }
        op.get_bind().execute(text('''
            DELETE FROM users
            WHERE surname = :surname
              AND name = :name
              AND second_name = :second_name
              AND employment_date = :employment_date
        '''), params)