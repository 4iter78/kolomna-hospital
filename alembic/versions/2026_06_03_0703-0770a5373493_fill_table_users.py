"""fill table users

Revision ID: 0770a5373493
Revises: 9dca9718e005
Create Date: 2026-06-03 07:03:40.580425

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0770a5373493'
down_revision: Union[str, Sequence[str], None] = '9dca9718e005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO users (
            surname,
            name,
            second_name,
            employment_date,
            login,
            password,
            user_role_id
        ) VALUES
            ('Смирнов',   'Павел',     'Евгеньевич',     '2015-06-01', 'smirnov_pe',   'secret_1',
                (SELECT id FROM user_roles WHERE name = 'Врач')),
            ('Федорова',  'Анна',      'Дмитриевна',     '2018-03-15', 'fedorova_ad',  'secret_2',
                (SELECT id FROM user_roles WHERE name = 'Врач')),
            ('Орлов',     'Николай',   'Сергеевич',      '2020-09-01', 'orlov_ns',     'secret_3',
                (SELECT id FROM user_roles WHERE name = 'Врач')),
            ('Захаров',   'Виктор',    'Геннадьевич',    '2014-04-01', 'zakharov_vg',  'secret_4',
                (SELECT id FROM user_roles WHERE name = 'Администратор')),
            ('Полякова',  'Кристина',  'Олеговна',       '2023-01-09', 'polyakova_ko', 'secret_5',
                (SELECT id FROM user_roles WHERE name = 'Гость')),
            -- Провизоры
            (
                'Ковалёва',
                'Марина',
                'Игоревна',
                '2019-02-11',
                'kovaleva_mi',
                'secret_6',
                (SELECT id FROM user_roles WHERE name = 'Провизор')
            ),
            (
                'Лебедев',
                'Артём',
                'Сергеевич',
                '2021-06-03',
                'lebedev_as',
                'secret_7',
                (SELECT id FROM user_roles WHERE name = 'Провизор')
            ),
            -- Кладовщики
            (
                'Морозов',
                'Дмитрий',
                'Валерьевич',
                '2018-09-17',
                'morozov_dv',
                'secret_8',
                (SELECT id FROM user_roles WHERE name = 'Кладовщик')
            ),
            (
                'Кузнецова',
                'Елена',
                'Павловна',
                '2020-12-01',
                'kuznetsova_ep',
                'secret_9',
                (SELECT id FROM user_roles WHERE name = 'Кладовщик')
            ),
            -- Медсестры
            (
                'Никитина',
                'Ольга',
                'Андреевна',
                '2017-05-22',
                'nikitina_oa',
                'secret_10',
                (SELECT id FROM user_roles WHERE name = 'Медсестра')
            ),
            (
                'Соколова',
                'Татьяна',
                'Викторовна',
                '2022-03-14',
                'sokolova_tv',
                'secret_11',
                (SELECT id FROM user_roles WHERE name = 'Медсестра')
            ),
            (
                'Власова',
                'Юлия',
                'Романовна',
                '2021-08-09',
                'vlasova_yr',
                'secret_12',
                (SELECT id FROM user_roles WHERE name = 'Медсестра')
            ),
            -- Фельдшеры
            (
                'Егоров',
                'Максим',
                'Ильич',
                '2016-01-18',
                'egorov_mi',
                'secret_13',
                (SELECT id FROM user_roles WHERE name = 'Фельдшер')
            ),
            (
                'Тарасова',
                'Наталья',
                'Олеговна',
                '2019-11-07',
                'tarasova_no',
                'secret_14',
                (SELECT id FROM user_roles WHERE name = 'Фельдшер')
            );
    """)


def downgrade() -> None:
    op.execute('''
            DELETE FROM users
            WHERE login IN (
                'smirnov_pe',
                'fedorova_ad',
                'orlov_ns',
                'zakharov_vg',
                'polyakova_ko',
                'kovaleva_mi',
                'lebedev_as',
                'morozov_dv',
                'kuznetsova_ep',
                'nikitina_oa',
                'sokolova_tv',
                'vlasova_yr',
                'egorov_mi',
                'tarasova_no'
            );
        ''')
