"""fill table department_to_user

Revision ID: ba776610b9b5
Revises: 4f048a2bf6be
Create Date: 2026-05-18 00:26:55.846254

"""
from typing import Sequence, Union

from sqlalchemy import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ba776610b9b5'
down_revision: Union[str, Sequence[str], None] = '4f048a2bf6be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO department_to_user (department_id, user_id)
        VALUES
            -- Врачи
            (
                (SELECT id FROM departments WHERE name = 'Приёмное отделение'),
                (SELECT id FROM users WHERE surname = 'Смирнов')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Стационарное отделение'),
                (SELECT id FROM users WHERE surname = 'Смирнов')
            ),
        
            (
                (SELECT id FROM departments WHERE name = 'Реанимация'),
                (SELECT id FROM users WHERE surname = 'Федорова')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Ожоговое отделение'),
                (SELECT id FROM users WHERE surname = 'Орлов')
            ),
            -- Регистратор
            (
                (SELECT id FROM departments WHERE name = 'Приёмное отделение'),
                (SELECT id FROM users WHERE surname = 'Белова')
            ),
            -- ИТ
            (
                (SELECT id FROM departments WHERE name = 'Отдел информационных технологий'),
                (SELECT id FROM users WHERE surname = 'Тихонов')
            ),
            -- Аспирант
            (
                (SELECT id FROM departments WHERE name = 'Стационарное отделение'),
                (SELECT id FROM users WHERE surname = 'Громова')
            ),
            -- Обслуживающий персонал
            (
                (SELECT id FROM departments WHERE name = 'Стационарное отделение'),
                (SELECT id FROM users WHERE surname = 'Денисов')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Приёмное отделение'),
                (SELECT id FROM users WHERE surname = 'Яковлева')
            ),
            -- Администратор
            (
                (SELECT id FROM departments WHERE name = 'Администрация'),
                (SELECT id FROM users WHERE surname = 'Захаров')
            ),
            -- Провизоры
            (
                (SELECT id FROM departments WHERE name = 'Аптека'),
                (SELECT id FROM users WHERE surname = 'Ковалёва')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Медицинский пункт'),
                (SELECT id FROM users WHERE surname = 'Лебедев')
            ),
            -- Кладовщики
            (
                (SELECT id FROM departments WHERE name = 'Склад'),
                (SELECT id FROM users WHERE surname = 'Морозов')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Склад'),
                (SELECT id FROM users WHERE surname = 'Кузнецова')
            ),
            -- Медсестры
            (
                (SELECT id FROM departments WHERE name = 'Стационарное отделение'),
                (SELECT id FROM users WHERE surname = 'Никитина')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Скорая'),
                (SELECT id FROM users WHERE surname = 'Соколова')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Реанимация'),
                (SELECT id FROM users WHERE surname = 'Власова')
            ),
            -- Фельдшеры
            (
                (SELECT id FROM departments WHERE name = 'Скорая'),
                (SELECT id FROM users WHERE surname = 'Егоров')
            ),
            (
                (SELECT id FROM departments WHERE name = 'Травматологический пункт'),
                (SELECT id FROM users WHERE surname = 'Тарасова')
            );
    ''')


def downgrade() -> None:
    # Полный список связей отделение -> пользователь для удаления:
    records_to_delete = [
        # Врачи
        ('Приёмное отделение', 'Смирнов'),
        ('Стационарное отделение', 'Смирнов'),
        ('Реанимация', 'Федорова'),
        ('Ожоговое отделение', 'Орлов'),
        # Регистратор
        ('Приёмное отделение', 'Белова'),
        # ИТ
        ('Отдел информационных технологий', 'Тихонов'),
        # Аспирант
        ('Стационарное отделение', 'Громова'),
        # Обслуживающий персонал
        ('Стационарное отделение', 'Денисов'),
        ('Приёмное отделение', 'Яковлева'),
        # Администратор
        ('Администрация', 'Захаров'),
        # Провизоры
        ('Аптека', 'Ковалёва'),
        ('Медицинский пункт', 'Лебедев'),
        # Кладовщики
        ('Склад', 'Морозов'),
        ('Склад', 'Кузнецова'),
        # Медсестры
        ('Стационарное отделение', 'Никитина'),
        ('Скорая', 'Соколова'),
        ('Реанимация', 'Власова'),
        # Фельдшеры
        ('Скорая', 'Егоров'),
        ('Травматологический пункт', 'Тарасова')
    ]

    for record in records_to_delete:
        department_name, user_surname = record

        # Параметры для подстановки в SQL-запрос
        params = {
            'department_name': department_name,
            'user_surname': user_surname
        }

        op.get_bind().execute(
            text('''
                DELETE FROM department_to_user
                WHERE department_id = (
                    SELECT id FROM departments
                    WHERE name = :department_name
                )
                AND user_id = (
                    SELECT id FROM users
                    WHERE surname = :user_surname
                )
            '''),
            params
        )
