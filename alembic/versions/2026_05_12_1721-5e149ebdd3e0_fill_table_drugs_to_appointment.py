"""fill table drugs_to_appointment

Revision ID: 5e149ebdd3e0
Revises: 92be3277ce80
Create Date: 2026-05-12 17:21:49.765492

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '5e149ebdd3e0'
down_revision: Union[str, Sequence[str], None] = '92be3277ce80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO drugs_to_appointment (drug_id, appointment_id) VALUES
    (
        (SELECT id FROM drugs WHERE name = 'Аспирин'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Смирнов'
           AND u.name = 'Павел'
           AND u.second_name = 'Евгеньевич'
           AND u.employment_date = '2015-06-01'
           AND p.surname = 'Иванов'
           AND p.name = 'Иван'
           AND p.second_name = 'Иванович'
           AND p.birth_date = '1980-03-15'
           AND hc.create_datetime = '2023-01-10 09:00:00'
           AND a.appointment_datetime = '2024-01-12 09:00:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Ибупрофен'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Смирнов'
           AND u.name = 'Павел'
           AND u.second_name = 'Евгеньевич'
           AND u.employment_date = '2015-06-01'
           AND p.surname = 'Иванов'
           AND p.name = 'Иван'
           AND p.second_name = 'Иванович'
           AND p.birth_date = '1980-03-15'
           AND hc.create_datetime = '2023-01-10 09:00:00'
           AND a.appointment_datetime = '2024-01-12 09:00:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Амоксициллин'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Федорова'
           AND u.name = 'Анна'
           AND u.second_name = 'Дмитриевна'
           AND u.employment_date = '2018-03-15'
           AND p.surname = 'Сидоров'
           AND p.name = 'Алексей'
           AND p.second_name = 'Петрович'
           AND p.birth_date = '1990-11-01'
           AND hc.create_datetime = '2023-02-01 08:45:00'
           AND a.appointment_datetime = '2024-01-14 11:00:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Омепразол'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Федорова'
           AND u.name = 'Анна'
           AND u.second_name = 'Дмитриевна'
           AND u.employment_date = '2018-03-15'
           AND p.surname = 'Кузнецова'
           AND p.name = 'Елена'
           AND p.second_name = 'Владимировна'
           AND p.birth_date = '1985-05-18'
           AND hc.create_datetime = '2023-02-20 11:00:00'
           AND a.appointment_datetime = '2024-01-15 09:30:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Метформин'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Орлов'
           AND u.name = 'Николай'
           AND u.second_name = 'Сергеевич'
           AND u.employment_date = '2020-09-01'
           AND p.surname = 'Новиков'
           AND p.name = 'Дмитрий'
           AND p.second_name = 'Андреевич'
           AND p.birth_date = '1968-09-30'
           AND hc.create_datetime = '2023-03-05 09:15:00'
           AND a.appointment_datetime = '2024-01-16 14:00:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Лизиноприл'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Смирнов'
           AND u.name = 'Павел'
           AND u.second_name = 'Евгеньевич'
           AND u.employment_date = '2015-06-01'
           AND p.surname = 'Морозова'
           AND p.name = 'Ольга'
           AND p.second_name = 'Николаевна'
           AND p.birth_date = '1992-02-14'
           AND hc.create_datetime = '2023-03-18 14:00:00'
           AND a.appointment_datetime = '2024-01-17 10:30:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Амброксол'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Орлов'
           AND u.name = 'Николай'
           AND u.second_name = 'Сергеевич'
           AND u.employment_date = '2020-09-01'
           AND p.surname = 'Волков'
           AND p.name = 'Сергей'
           AND p.second_name = 'Михайлович'
           AND p.birth_date = '1955-12-05'
           AND hc.create_datetime = '2023-04-02 10:00:00'
           AND a.appointment_datetime = '2024-01-18 08:00:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Аторвастатин'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Смирнов'
           AND u.name = 'Павел'
           AND u.second_name = 'Евгеньевич'
           AND u.employment_date = '2015-06-01'
           AND p.surname = 'Лебедев'
           AND p.name = 'Андрей'
           AND p.second_name = 'Олегович'
           AND p.birth_date = '1978-04-10'
           AND hc.create_datetime = '2023-05-10 09:00:00'
           AND a.appointment_datetime = '2024-01-20 11:00:00')
    ),
    (
          (SELECT id FROM drugs WHERE name = 'Цетиризин'),
          (SELECT a.id FROM appointments a
           JOIN users u ON a.user_id = u.id
           JOIN health_cards hc ON a.health_card_id = hc.id
           JOIN patients p ON hc.patient_id = p.id
           WHERE u.surname = 'Федорова'
             AND u.name = 'Анна'
             AND u.second_name = 'Дмитриевна'
             AND u.employment_date = '2018-03-15'
             AND p.surname = 'Зайцева'
             AND p.name = 'Наталья'
             AND p.second_name = 'Юрьевна'
             AND p.birth_date = '2000-06-25'
             AND hc.create_datetime = '2023-04-25 13:30:00'
             AND a.appointment_datetime = '2024-01-19 13:00:00')
    ),
    (
        (SELECT id FROM drugs WHERE name = 'Диклофенак'),
        (SELECT a.id FROM appointments a
         JOIN users u ON a.user_id = u.id
         JOIN health_cards hc ON a.health_card_id = hc.id
         JOIN patients p ON hc.patient_id = p.id
         WHERE u.surname = 'Орлов'
           AND u.name = 'Николай'
           AND u.second_name = 'Сергеевич'
           AND u.employment_date = '2020-09-01'
           AND p.surname = 'Козлова'
           AND p.name = 'Татьяна'
           AND p.second_name = 'Ивановна'
           AND p.birth_date = '1963-08-19'
           AND hc.create_datetime = '2023-05-22 11:45:00'
           AND a.appointment_datetime = '2024-01-21 15:00:00')
    );
    ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('Аспирин', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Иванов', 'Иван', 'Иванович', '1980-03-15', '2023-01-10 09:00:00', '2024-01-12 09:00:00'),
        ('Ибупрофен', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Иванов', 'Иван', 'Иванович', '1980-03-15', '2023-01-10 09:00:00', '2024-01-12 09:00:00'),
        ('Амоксициллин', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'Сидоров', 'Алексей', 'Петрович', '1990-11-01', '2023-02-01 08:45:00', '2024-01-14 11:00:00'),
        ('Омепразол', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'Кузнецова', 'Елена', 'Владимировна', '1985-05-18', '2023-02-20 11:00:00', '2024-01-15 09:30:00'),
        ('Метформин', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'Новиков', 'Дмитрий', 'Андреевич', '1968-09-30', '2023-03-05 09:15:00', '2024-01-16 14:00:00'),
        ('Лизиноприл', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Морозова', 'Ольга', 'Николаевна', '1992-02-14', '2023-03-18 14:00:00', '2024-01-17 10:30:00'),
        ('Амброксол', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'Волков', 'Сергей', 'Михайлович', '1955-12-05', '2023-04-02 10:00:00', '2024-01-18 08:00:00'),
        ('Аторвастатин', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01', 'Лебедев', 'Андрей', 'Олегович', '1978-04-10', '2023-05-10 09:00:00', '2024-01-20 11:00:00'),
        ('Цетиризин', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15', 'Зайцева', 'Наталья', 'Юрьевна', '2000-06-25', '2023-04-25 13:30:00', '2024-01-19 13:00:00'),
        ('Диклофенак', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01', 'Козлова', 'Татьяна', 'Ивановна', '1963-08-19', '2023-05-22 11:45:00', '2024-01-21 15:00:00')
    ]

    for drug_name, u_surname, u_name, u_second_name, u_employment_date, p_surname, p_name, p_second_name, p_birth_date, hc_create_datetime, a_appointment_datetime in records_to_delete:
        params = {
            'drug_name': drug_name,
            'u_surname': u_surname,
            'u_name': u_name,
            'u_second_name': u_second_name,
            'u_employment_date': u_employment_date,
            'p_surname': p_surname,
            'p_name': p_name,
            'p_second_name': p_second_name,
            'p_birth_date': p_birth_date,
            'hc_create_datetime': hc_create_datetime,
            'a_appointment_datetime': a_appointment_datetime
        }

        op.get_bind().execute(
            text('''
                DELETE FROM drugs_to_appointment
                WHERE
                    drug_id = (SELECT id FROM drugs WHERE name = :drug_name)
                    AND appointment_id = (
                        SELECT a.id FROM appointments a
                        JOIN users u ON a.user_id = u.id
                        JOIN health_cards hc ON a.health_card_id = hc.id
                        JOIN patients p ON hc.patient_id = p.id
                        WHERE u.surname = :u_surname
                          AND u.name = :u_name
                          AND u.second_name = :u_second_name
                          AND u.employment_date = :u_employment_date
                          AND p.surname = :p_surname
                          AND p.name = :p_name
                          AND p.second_name = :p_second_name
                          AND p.birth_date = :p_birth_date
                          AND hc.create_datetime = :hc_create_datetime
                          AND a.appointment_datetime = :a_appointment_datetime
            )
            '''),
            params
        )

