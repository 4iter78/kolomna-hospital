"""fill table comments

Revision ID: e5ab770ca3b9
Revises: 0ce551bc29c7
Create Date: 2026-05-12 19:39:08.523205

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'e5ab770ca3b9'
down_revision: Union[str, Sequence[str], None] = '0ce551bc29c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO comments (from_patient_id, description, date, to_user_id)
VALUES
    ((SELECT id FROM patients
      WHERE surname = 'Иванов'
        AND name = 'Иван'
        AND second_name = 'Иванович'
        AND birth_date = '1980-03-15'),
     'Отличный специалист, всё подробно объяснил.',
     '2024-01-13',
     (SELECT id FROM users
      WHERE surname = 'Смирнов'
        AND name = 'Павел'
        AND second_name = 'Евгеньевич'
        AND employment_date = '2015-06-01')),
    ((SELECT id FROM patients
      WHERE surname = 'Петрова'
        AND name = 'Мария'
        AND second_name = 'Сергеевна'
        AND birth_date = '1975-07-22'),
     'Долгое ожидание в очереди, но врач грамотный.',
     '2024-01-14',
     (SELECT id FROM users
      WHERE surname = 'Смирнов'
        AND name = 'Павел'
        AND second_name = 'Евгеньевич'
        AND employment_date = '2015-06-01')),
    ((SELECT id FROM patients
      WHERE surname = 'Сидоров'
        AND name = 'Алексей'
        AND second_name = 'Петрович'
        AND birth_date = '1990-11-01'),
     'Очень внимательный доктор, спасибо!',
     '2024-01-15',
     (SELECT id FROM users
      WHERE surname = 'Федорова'
        AND name = 'Анна'
        AND second_name = 'Дмитриевна'
        AND employment_date = '2018-03-15')),
    ((SELECT id FROM patients
      WHERE surname = 'Кузнецова'
        AND name = 'Елена'
        AND second_name = 'Владимировна'
        AND birth_date = '1985-05-18'),
     'Назначенное лечение помогло быстро.',
     '2024-01-16',
     (SELECT id FROM users
      WHERE surname = 'Федорова'
        AND name = 'Анна'
        AND second_name = 'Дмитриевна'
        AND employment_date = '2018-03-15')),
    ((SELECT id FROM patients
      WHERE surname = 'Новиков'
        AND name = 'Дмитрий'
        AND second_name = 'Андреевич'
        AND birth_date = '1968-09-30'),
     'Хотелось бы более подробных разъяснений по диагнозу.',
     '2024-01-17',
     (SELECT id FROM users
      WHERE surname = 'Орлов'
        AND name = 'Николай'
        AND second_name = 'Сергеевич'
        AND employment_date = '2020-09-01')),
    ((SELECT id FROM patients
      WHERE surname = 'Морозова'
        AND name = 'Ольга'
        AND second_name = 'Николаевна'
        AND birth_date = '1992-02-14'),
     'Приём прошёл быстро и профессионально.',
     '2024-01-18',
     (SELECT id FROM users
      WHERE surname = 'Смирнов'
        AND name = 'Павел'
        AND second_name = 'Евгеньевич'
        AND employment_date = '2015-06-01')),
    ((SELECT id FROM patients
      WHERE surname = 'Волков'
        AND name = 'Сергей'
        AND second_name = 'Михайлович'
        AND birth_date = '1955-12-05'),
     'Доктор внушает доверие, рекомендую.',
     '2024-01-19',
     (SELECT id FROM users
      WHERE surname = 'Орлов'
        AND name = 'Николай'
        AND second_name = 'Сергеевич'
        AND employment_date = '2020-09-01')),
    ((SELECT id FROM patients
      WHERE surname = 'Зайцева'
        AND name = 'Наталья'
        AND second_name = 'Юрьевна'
        AND birth_date = '2000-06-25'),
     'Спасибо за чуткость и понимание.',
     '2024-01-20',
     (SELECT id FROM users
      WHERE surname = 'Федорова'
        AND name = 'Анна'
        AND second_name = 'Дмитриевна'
        AND employment_date = '2018-03-15')),
    ((SELECT id FROM patients
      WHERE surname = 'Лебедев'
        AND name = 'Андрей'
        AND second_name = 'Олегович'
        AND birth_date = '1978-04-10'),
     'Всё понравилось, лечение эффективное.',
     '2024-01-21',
     (SELECT id FROM users
      WHERE surname = 'Смирнов'
        AND name = 'Павел'
        AND second_name = 'Евгеньевич'
        AND employment_date = '2015-06-01')),
    ((SELECT id FROM patients
      WHERE surname = 'Козлова'
        AND name = 'Татьяна'
        AND second_name = 'Ивановна'
        AND birth_date = '1963-08-19'),
     'Немного не хватило времени на консультацию.',
     '2024-01-22',
     (SELECT id FROM users
      WHERE surname = 'Орлов'
        AND name = 'Николай'
        AND second_name = 'Сергеевич'
        AND employment_date = '2020-09-01'));
    ''')


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Иванов', 'Иван', 'Иванович', '1980-03-15',
         'Отличный специалист, всё подробно объяснил.', '2024-01-13',
         'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Петрова', 'Мария', 'Сергеевна', '1975-07-22',
         'Долгое ожидание в очереди, но врач грамотный.', '2024-01-14',
         'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Сидоров', 'Алексей', 'Петрович', '1990-11-01',
         'Очень внимательный доктор, спасибо!', '2024-01-15',
         'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Кузнецова', 'Елена', 'Владимировна', '1985-05-18',
         'Назначенное лечение помогло быстро.', '2024-01-16',
         'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Новиков', 'Дмитрий', 'Андреевич', '1968-09-30',
         'Хотелось бы более подробных разъяснений по диагнозу.', '2024-01-17',
         'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Морозова', 'Ольга', 'Николаевна', '1992-02-14',
         'Приём прошёл быстро и профессионально.', '2024-01-18',
         'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Волков', 'Сергей', 'Михайлович', '1955-12-05',
         'Доктор внушает доверие, рекомендую.', '2024-01-19',
         'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('Зайцева', 'Наталья', 'Юрьевна', '2000-06-25',
         'Спасибо за чуткость и понимание.', '2024-01-20',
         'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('Лебедев', 'Андрей', 'Олегович', '1978-04-10',
         'Всё понравилось, лечение эффективное.', '2024-01-21',
         'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('Козлова', 'Татьяна', 'Ивановна', '1963-08-19',
         'Немного не хватило времени на консультацию.', '2024-01-22',
         'Орлов', 'Николай', 'Сергеевич', '2020-09-01')
    ]

    for record in records_to_delete:
        p_surname, p_name, p_second_name, p_birth_date, \
        description, date, \
        u_surname, u_name, u_second_name, u_employment_date = record

        # Выносим все параметры в отдельный словарь
        params = {
            'p_surname': p_surname,
            'p_name': p_name,
            'p_second_name': p_second_name,
            'p_birth_date': p_birth_date,
            'description': description,
            'date': date,
            'u_surname': u_surname,
            'u_name': u_name,
            'u_second_name': u_second_name,
            'u_employment_date': u_employment_date
        }

        op.get_bind().execute(
            text('''
            DELETE FROM comments
            WHERE from_patient_id = (
                SELECT id FROM patients
                WHERE surname = :p_surname
                  AND name = :p_name
                  AND second_name = :p_second_name
                  AND birth_date = :p_birth_date
            )
            AND description = :description
            AND date = :date
            AND to_user_id = (
                SELECT id FROM users
                WHERE surname = :u_surname
                  AND name = :u_name
                  AND second_name = :u_second_name
                  AND employment_date = :u_employment_date
            )
            '''), params
        )
