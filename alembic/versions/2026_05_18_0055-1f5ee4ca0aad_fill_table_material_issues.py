"""fill table material_issues

Revision ID: 1f5ee4ca0aad
Revises: 02d6c24677a4
Create Date: 2026-05-18 00:55:40.662034

"""
from typing import Sequence, Union

from sqlalchemy import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1f5ee4ca0aad'
down_revision: Union[str, Sequence[str], None] = '02d6c24677a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO material_issues (
            from_user_id,
            to_user_id,
            issue_date,
            notes
        )
        VALUES
            (
                (SELECT id FROM users WHERE surname = 'Морозов'),
                (SELECT id FROM users WHERE surname = 'Смирнов'),
                NOW() - INTERVAL '5 day',
                'Выдача в приёмное отделение'
            ),
        
            (
                (SELECT id FROM users WHERE surname = 'Кузнецова'),
                (SELECT id FROM users WHERE surname = 'Федорова'),
                NOW() - INTERVAL '2 day',
                'Выдача в реанимацию'
            );
    ''')


def downgrade() -> None:
    # Полный список записей material_issues для удаления:
    records_to_delete = [
        (
            'Морозов',
            'Смирнов',
            'Выдача в приёмное отделение'
        ),
        (
            'Кузнецова',
            'Федорова',
            'Выдача в реанимацию'
        )
    ]

    for record in records_to_delete:
        from_user_surname, to_user_surname, notes = record

        # Параметры для подстановки в SQL-запрос
        params = {
            'from_user_surname': from_user_surname,
            'to_user_surname': to_user_surname,
            'notes': notes
        }

        op.get_bind().execute(
            text('''
                DELETE FROM material_issues
                WHERE from_user_id = (
                    SELECT id
                    FROM users
                    WHERE surname = :from_user_surname
                )
                AND to_user_id = (
                    SELECT id
                    FROM users
                    WHERE surname = :to_user_surname
                )
                AND notes = :notes
            '''),
            params
        )
