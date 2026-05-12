"""fill table training_to_user

Revision ID: b89bbcd1db05
Revises: 5e149ebdd3e0
Create Date: 2026-05-12 18:57:20.304674

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'b89bbcd1db05'
down_revision: Union[str, Sequence[str], None] = '5e149ebdd3e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO training_to_user (training_id, user_id)
VALUES
    ((SELECT id FROM training WHERE name = 'Работа с аппаратом МРТ: базовый курс'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM training WHERE name = 'Работа с аппаратом МРТ: продвинутый курс'),
     (SELECT id FROM users WHERE surname = 'Смирнов' AND name = 'Павел' AND second_name = 'Евгеньевич' AND employment_date = '2015-06-01')),
    ((SELECT id FROM training WHERE name = 'Рентген-диагностика: основы'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM training WHERE name = 'Рентген-диагностика: интерпретация снимков'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15')),
    ((SELECT id FROM training WHERE name = 'Флюорография: техника проведения'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM training WHERE name = 'Флюорография: безопасность и дозиметрия'),
     (SELECT id FROM users WHERE surname = 'Орлов' AND name = 'Николай' AND second_name = 'Сергеевич' AND employment_date = '2020-09-01')),
    ((SELECT id FROM training WHERE name = 'Работа с аппаратом МРТ: базовый курс'),
     (SELECT id FROM users WHERE surname = 'Громова' AND name = 'Ирина' AND second_name = 'Петровна' AND employment_date = '2016-11-01')),
    ((SELECT id FROM training WHERE name = 'Рентген-диагностика: основы'),
     (SELECT id FROM users WHERE surname = 'Громова' AND name = 'Ирина' AND second_name = 'Петровна' AND employment_date = '2016-11-01')),
    ((SELECT id FROM training WHERE name = 'Флюорография: техника проведения'),
     (SELECT id FROM users WHERE surname = 'Громова' AND name = 'Ирина' AND second_name = 'Петровна' AND employment_date = '2016-11-01')),
    ((SELECT id FROM training WHERE name = 'Работа с аппаратом МРТ: продвинутый курс'),
     (SELECT id FROM users WHERE surname = 'Федорова' AND name = 'Анна' AND second_name = 'Дмитриевна' AND employment_date = '2018-03-15'));
    ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Работа с аппаратом МРТ: базовый курс', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Работа с аппаратом МРТ: продвинутый курс', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Рентген-диагностика: основы', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Рентген-диагностика: интерпретация снимков', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Флюорография: техника проведения', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Флюорография: безопасность и дозиметрия', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Работа с аппаратом МРТ: базовый курс', 'Громова', 'Ирина', 'Петровна', '2016-11-01'),
        ('Рентген-диагностика: основы', 'Громова', 'Ирина', 'Петровна', '2016-11-01'),
        ('Флюорография: техника проведения', 'Громова', 'Ирина', 'Петровна', '2016-11-01'),
        ('Работа с аппаратом МРТ: продвинутый курс', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15')
    ]

    for record in records_to_delete:
        training_name, surname, name, second_name, employment_date = record

        # Выносим все параметры в отдельный словарь
        params = {
            'training_name': training_name,
            'surname': surname,
            'name': name,
            'second_name': second_name,
            'employment_date': employment_date
        }

        op.get_bind().execute(
            text('''
            DELETE FROM training_to_user
            WHERE training_id = (
                SELECT id FROM training
                WHERE name = :training_name
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
