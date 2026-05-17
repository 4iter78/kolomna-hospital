"""fill table users

Revision ID: dbc1608e0db8
Revises: 0845c8fdc149
Create Date: 2026-05-18 00:22:19.532125

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dbc1608e0db8'
down_revision: Union[str, Sequence[str], None] = '0845c8fdc149'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO users (
            surname,
            name,
            second_name,
            employment_date,
            user_role_id,
            login,
            password
        )
        VALUES
            -- Провизоры
            (
                'Ковалёва',
                'Марина',
                'Игоревна',
                '2019-02-11',
                (SELECT id FROM user_roles WHERE name = 'Провизор'),
                'kovaleva_mi',
                'secret_11'
            ),
            (
                'Лебедев',
                'Артём',
                'Сергеевич',
                '2021-06-03',
                (SELECT id FROM user_roles WHERE name = 'Провизор'),
                'lebedev_as',
                'secret_12'
            ),
            -- Кладовщики
            (
                'Морозов',
                'Дмитрий',
                'Валерьевич',
                '2018-09-17',
                (SELECT id FROM user_roles WHERE name = 'Кладовщик'),
                'morozov_dv',
                'secret_13'
            ),
            (
                'Кузнецова',
                'Елена',
                'Павловна',
                '2020-12-01',
                (SELECT id FROM user_roles WHERE name = 'Кладовщик'),
                'kuznetsova_ep',
                'secret_14'
            ),
            -- Медсестры
            (
                'Никитина',
                'Ольга',
                'Андреевна',
                '2017-05-22',
                (SELECT id FROM user_roles WHERE name = 'Медсестра'),
                'nikitina_oa',
                'secret_15'
            ),
            (
                'Соколова',
                'Татьяна',
                'Викторовна',
                '2022-03-14',
                (SELECT id FROM user_roles WHERE name = 'Медсестра'),
                'sokolova_tv',
                'secret_16'
            ),
            (
                'Власова',
                'Юлия',
                'Романовна',
                '2021-08-09',
                (SELECT id FROM user_roles WHERE name = 'Медсестра'),
                'vlasova_yr',
                'secret_17'
            ),
            -- Фельдшеры
            (
                'Егоров',
                'Максим',
                'Ильич',
                '2016-01-18',
                (SELECT id FROM user_roles WHERE name = 'Фельдшер'),
                'egorov_mi',
                'secret_18'
            ),
            (
                'Тарасова',
                'Наталья',
                'Олеговна',
                '2019-11-07',
                (SELECT id FROM user_roles WHERE name = 'Фельдшер'),
                'tarasova_no',
                'secret_19'
            );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM users
        WHERE login IN (
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
