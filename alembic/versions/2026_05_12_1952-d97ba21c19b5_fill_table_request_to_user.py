"""fill table request_to_user

Revision ID: d97ba21c19b5
Revises: 6687b1e4c601
Create Date: 2026-05-12 19:52:38.211900

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'd97ba21c19b5'
down_revision: Union[str, Sequence[str], None] = '6687b1e4c601'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    INSERT INTO request_to_user (request_id, user_id)
VALUES
    ((SELECT id FROM requests WHERE request_file = 'requests/req_001.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Смирнов'
        AND name = 'Павел'
        AND second_name = 'Евгеньевич'
        AND employment_date = '2015-06-01')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_002.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Федорова'
        AND name = 'Анна'
        AND second_name = 'Дмитриевна'
        AND employment_date = '2018-03-15')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_003.docx'),
     (SELECT id FROM users
      WHERE surname = 'Орлов'
        AND name = 'Николай'
        AND second_name = 'Сергеевич'
        AND employment_date = '2020-09-01')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_004.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Белова'
        AND name = 'Светлана'
        AND second_name = 'Александровна'
        AND employment_date = '2017-01-10')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_005.docx'),
     (SELECT id FROM users
      WHERE surname = 'Тихонов'
        AND name = 'Игорь'
        AND second_name = 'Васильевич'
        AND employment_date = '2019-05-20')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_006.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Громова'
        AND name = 'Ирина'
        AND second_name = 'Петровна'
        AND employment_date = '2016-11-01')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_007.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Денисов'
        AND name = 'Антон'
        AND second_name = 'Романович'
        AND employment_date = '2021-02-28')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_008.docx'),
     (SELECT id FROM users
      WHERE surname = 'Яковлева'
        AND name = 'Людмила'
        AND second_name = 'Борисовна'
        AND employment_date = '2022-07-15')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_009.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Захаров'
        AND name = 'Виктор'
        AND second_name = 'Геннадьевич'
        AND employment_date = '2014-04-01')),
    ((SELECT id FROM requests WHERE request_file = 'requests/req_010.pdf'),
     (SELECT id FROM users
      WHERE surname = 'Полякова'
        AND name = 'Кристина'
        AND second_name = 'Олеговна'
        AND employment_date = '2023-01-09'));
    ''')
    pass


def downgrade() -> None:
    # Полный список данных для точного удаления
    records_to_delete = [
        ('requests/req_001.pdf', 'Смирнов', 'Павел', 'Евгеньевич', '2015-06-01'),
        ('requests/req_002.pdf', 'Федорова', 'Анна', 'Дмитриевна', '2018-03-15'),
        ('requests/req_003.docx', 'Орлов', 'Николай', 'Сергеевич', '2020-09-01'),
        ('requests/req_004.pdf', 'Белова', 'Светлана', 'Александровна', '2017-01-10'),
        ('requests/req_005.docx', 'Тихонов', 'Игорь', 'Васильевич', '2019-05-20'),
        ('requests/req_006.pdf', 'Громова', 'Ирина', 'Петровна', '2016-11-01'),
        ('requests/req_007.pdf', 'Денисов', 'Антон', 'Романович', '2021-02-28'),
        ('requests/req_008.docx', 'Яковлева', 'Людмила', 'Борисовна', '2022-07-15'),
        ('requests/req_009.pdf', 'Захаров', 'Виктор', 'Геннадьевич', '2014-04-01'),
        ('requests/req_010.pdf', 'Полякова', 'Кристина', 'Олеговна', '2023-01-09')
    ]

    for record in records_to_delete:
        request_file, u_surname, u_name, u_second_name, u_employment_date = record

        # Выносим все параметры в отдельный словарь
        params = {
            'request_file': request_file,
            'u_surname': u_surname,
            'u_name': u_name,
            'u_second_name': u_second_name,
            'u_employment_date': u_employment_date
        }

        op.get_bind().execute(
            text('''
            DELETE FROM request_to_user
            WHERE request_id = (
                SELECT id FROM requests
                WHERE request_file = :request_file
            )
            AND user_id = (
                SELECT id FROM users
                WHERE surname = :u_surname
                  AND name = :u_name
                  AND second_name = :u_second_name
                  AND employment_date = :u_employment_date
            )
            '''), params
        )
