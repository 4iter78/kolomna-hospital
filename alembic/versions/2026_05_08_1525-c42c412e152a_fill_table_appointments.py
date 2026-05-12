"""fill table appointments

Revision ID: c42c412e152a
Revises: b2869e6129bb
Create Date: 2026-05-08 15:25:36.420117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'c42c412e152a'
down_revision: Union[str, Sequence[str], None] = 'b2869e6129bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO appointments (user_id, health_card_id, treatment_type_id, appointment_datetime, diagnosis_id) VALUES
    (
        (SELECT id FROM users
         WHERE surname = 'Смирнов'
           AND name = 'Павел'
           AND second_name = 'Евгеньевич'
           AND employment_date = '2015-06-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Иванов'
           AND p.name = 'Иван'
           AND p.second_name = 'Иванович'
           AND p.birth_date = '1980-03-15'
           AND hc.create_datetime = '2023-01-10 09:00:00'),
        (SELECT id FROM treatment_types WHERE name = 'Амбулаторно'),
        '2024-01-12 09:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Гипертония')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Смирнов'
           AND name = 'Павел'
           AND second_name = 'Евгеньевич'
           AND employment_date = '2015-06-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Петрова'
           AND p.name = 'Мария'
           AND p.second_name = 'Сергеевна'
           AND p.birth_date = '1975-07-22'
           AND hc.create_datetime = '2023-01-15 10:30:00'),
        (SELECT id FROM treatment_types WHERE name = 'Амбулаторно'),
        '2024-01-13 10:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Острый бронхит')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Федорова'
           AND name = 'Анна'
           AND second_name = 'Дмитриевна'
           AND employment_date = '2018-03-15'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Сидоров'
           AND p.name = 'Алексей'
           AND p.second_name = 'Петрович'
           AND p.birth_date = '1990-11-01'
           AND hc.create_datetime = '2023-02-01 08:45:00'),
        (SELECT id FROM treatment_types WHERE name = 'Стационар'),
        '2024-01-14 11:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Пневмония')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Федорова'
           AND name = 'Анна'
           AND second_name = 'Дмитриевна'
           AND employment_date = '2018-03-15'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Кузнецова'
           AND p.name = 'Елена'
           AND p.second_name = 'Владимировна'
           AND p.birth_date = '1985-05-18'
           AND hc.create_datetime = '2023-02-20 11:00:00'),
        (SELECT id FROM treatment_types WHERE name = 'Амбулаторно'),
        '2024-01-15 09:30:00',
        (SELECT id FROM diagnosises WHERE name = 'Гастрит')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Орлов'
           AND name = 'Николай'
           AND second_name = 'Сергеевич'
           AND employment_date = '2020-09-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Новиков'
           AND p.name = 'Дмитрий'
           AND p.second_name = 'Андреевич'
           AND p.birth_date = '1968-09-30'
           AND hc.create_datetime = '2023-03-05 09:15:00'),
        (SELECT id FROM treatment_types WHERE name = 'Дневной стационар'),
        '2024-01-16 14:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Сахарный диабет 2 типа')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Смирнов'
           AND name = 'Павел'
           AND second_name = 'Евгеньевич'
           AND employment_date = '2015-06-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Морозова'
           AND p.name = 'Ольга'
           AND p.second_name = 'Николаевна'
           AND p.birth_date = '1992-02-14'
           AND hc.create_datetime = '2023-03-18 14:00:00'),
        (SELECT id FROM treatment_types WHERE name = 'Амбулаторно'),
        '2024-01-17 10:30:00',
        (SELECT id FROM diagnosises WHERE name = 'ОРВИ')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Орлов'
           AND name = 'Николай'
           AND second_name = 'Сергеевич'
           AND employment_date = '2020-09-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Волков'
           AND p.name = 'Сергей'
           AND p.second_name = 'Михайлович'
           AND p.birth_date = '1955-12-05'
           AND hc.create_datetime = '2023-04-02 10:00:00'),
        (SELECT id FROM treatment_types WHERE name = 'Госпитализация'),
        '2024-01-18 08:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Остеохондроз')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Федорова'
           AND name = 'Анна'
           AND second_name = 'Дмитриевна'
           AND employment_date = '2018-03-15'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Зайцева'
           AND p.name = 'Наталья'
           AND p.second_name = 'Юрьевна'
           AND p.birth_date = '2000-06-25'
           AND hc.create_datetime = '2023-04-25 13:30:00'),
        (SELECT id FROM treatment_types WHERE name = 'Амбулаторно'),
        '2024-01-19 13:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Мигрень')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Смирнов'
           AND name = 'Павел'
           AND second_name = 'Евгеньевич'
           AND employment_date = '2015-06-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Лебедев'
           AND p.name = 'Андрей'
           AND p.second_name = 'Олегович'
           AND p.birth_date = '1978-04-10'
           AND hc.create_datetime = '2023-05-10 09:00:00'),
        (SELECT id FROM treatment_types WHERE name = 'Стационар'),
        '2024-01-20 11:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Анемия')
    ),
    (
        (SELECT id FROM users
         WHERE surname = 'Орлов'
           AND name = 'Николай'
           AND second_name = 'Сергеевич'
           AND employment_date = '2020-09-01'),
        (SELECT hc.id FROM health_cards hc
         JOIN patients p ON hc.patient_id = p.id
         WHERE p.surname = 'Козлова'
           AND p.name = 'Татьяна'
           AND p.second_name = 'Ивановна'
           AND p.birth_date = '1963-08-19'
           AND hc.create_datetime = '2023-05-22 11:45:00'),
        (SELECT id FROM treatment_types WHERE name = 'Амбулаторно'),
        '2024-01-21 15:00:00',
        (SELECT id FROM diagnosises WHERE name = 'Артрит')
    );
    ''')
    pass

def downgrade() -> None:
    # Полный список данных для точного удаления записей из appointments
    records_to_delete = [
        ('Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Иванов', 'Иван', 'Иванович', '1980-03-15', '2023-01-10 09:00:00', '2024-01-12 09:00:00'),
        ('Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Петрова', 'Мария', 'Сергеевна', '1975-07-22', '2023-01-15 10:30:00', '2024-01-13 10:00:00'),
        ('Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'Сидоров', 'Алексей', 'Петрович', '1990-11-01', '2023-02-01 08:45:00', '2024-01-14 11:00:00'),
        ('Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'Кузнецова', 'Елена', 'Владимировна', '1985-05-18', '2023-02-20 11:00:00', '2024-01-15 09:30:00'),
        ('Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'Новиков', 'Дмитрий', 'Андреевич', '1968-09-30', '2023-03-05 09:15:00', '2024-01-16 14:00:00'),
        ('Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Морозова', 'Ольга', 'Николаевна', '1992-02-14', '2023-03-18 14:00:00', '2024-01-17 10:30:00'),
        ('Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'Волков', 'Сергей', 'Михайлович', '1955-12-05', '2023-04-02 10:00:00', '2024-01-18 08:00:00'),
        ('Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'Зайцева', 'Наталья', 'Юрьевна', '2000-06-25', '2023-04-25 13:30:00', '2024-01-19 13:00:00'),
        ('Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Лебедев', 'Андрей', 'Олегович', '1978-04-10', '2023-05-10 09:00:00', '2024-01-20 11:00:00'),
        ('Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'Козлова', 'Татьяна', 'Ивановна', '1963-08-19', '2023-05-22 11:45:00', '2024-01-21 15:00:00')
    ]

    for record in records_to_delete:
        (user_surname, user_name, user_second_name, user_employment_date,
         patient_surname, patient_name, patient_second_name, patient_birth_date,
         health_card_create_datetime, appointment_datetime) = record

        # Формируем словарь параметров для именованных плейсхолдеров
        params = {
            'user_surname': user_surname,
            'user_name': user_name,
            'user_second_name': user_second_name,
            'user_employment_date': user_employment_date,
            'patient_surname': patient_surname,
            'patient_name': patient_name,
            'patient_second_name': patient_second_name,
            'patient_birth_date': patient_birth_date,
            'health_card_create_datetime': health_card_create_datetime,
            'appointment_datetime': appointment_datetime
        }

        op.get_bind().execute(
            text('''
            DELETE FROM appointments
            WHERE
                user_id = (
                    SELECT id FROM users
            WHERE surname = :user_surname
              AND name = :user_name
              AND second_name = :user_second_name
              AND employment_date = :user_employment_date
        )
        AND health_card_id = (
            SELECT hc.id FROM health_cards hc
            JOIN patients p ON hc.patient_id = p.id
            WHERE p.surname = :patient_surname
              AND p.name = :patient_name
              AND p.second_name = :patient_second_name
              AND p.birth_date = :patient_birth_date
              AND hc.create_datetime = :health_card_create_datetime
        )
        AND appointment_datetime = :appointment_datetime
            '''), params
        )


