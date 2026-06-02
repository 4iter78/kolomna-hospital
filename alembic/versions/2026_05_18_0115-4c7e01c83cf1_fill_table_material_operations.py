"""fill table material_operations

Revision ID: 4c7e01c83cf1
Revises: b43f943c21eb
Create Date: 2026-06-01 04:46:11.292161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '4c7e01c83cf1'
down_revision: Union[str, Sequence[str], None] = 'b43f943c21eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO material_operations (
            medical_material_id,
            department_id,
            quantity,
            document_number,
            current_user_id,
            operation_date,
            description,
            is_issued,
            is_written_off
        )
        VALUES
        (
            (SELECT id FROM medical_materials WHERE name = 'Бинт стерильный'),
            (SELECT id FROM departments WHERE name = 'Приёмное отделение'),
            10,
            'REQ-001',
            (SELECT id FROM users WHERE surname = 'Смирнов'),
            NOW() - INTERVAL '1 day',
            'Выдано пациентам',
            TRUE,
            FALSE
        ),
        (
            (SELECT id FROM medical_materials WHERE name = 'Медицинские перчатки'),
            (SELECT id FROM departments WHERE name = 'Приёмное отделение'),
            20,
            'REQ-002',
            (SELECT id FROM users WHERE surname = 'Федорова'),
            NOW() - INTERVAL '12 hour',
            'Использовано в отделении',
            TRUE,
            FALSE
        ),
        (
            (SELECT id FROM medical_materials WHERE name = 'Физраствор 0.9%'),
            (SELECT id FROM departments WHERE name = 'Приёмное отделение'),
            5,
            'WO-001',
            (SELECT id FROM users WHERE surname = 'Морозов'),
            NOW() - INTERVAL '3 day',
            'Повреждена упаковка',
            FALSE,
            TRUE
        ),
        (
            (SELECT id FROM medical_materials WHERE name = 'Лидокаин'),
            (SELECT id FROM departments WHERE name = 'Реанимация'),
            2,
            'WO-002',
            (SELECT id FROM users WHERE surname = 'Кузнецова'),
            NOW() - INTERVAL '1 day',
            'Истёк срок годности',
            FALSE,
            TRUE
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    records_to_delete = [
        (
            'Бинт стерильный',
            'Приёмное отделение',
            10,
            'REQ-001',
            'Смирнов',
            'Выдано пациентам',
            True,
            False
        ),
        (
            'Медицинские перчатки',
            'Приёмное отделение',
            20,
            'REQ-002',
            'Федорова',
            'Использовано в отделении',
            True,
            False
        ),
        (
            'Физраствор 0.9%',
            'Приёмное отделение',
            5,
            'WO-001',
            'Морозов',
            'Повреждена упаковка',
            False,
            True
        ),
        (
            'Лидокаин',
            'Реанимация',
            2,
            'WO-002',
            'Кузнецова',
            'Истёк срок годности',
            False,
            True
        )
    ]

    for record in records_to_delete:
        (
            material_name,
            department_name,
            quantity,
            document_number,
            user_surname,
            description,
            is_issued,
            is_written_off
        ) = record

        params = {
            'material_name': material_name,
            'department_name': department_name,
            'quantity': quantity,
            'document_number': document_number,
            'user_surname': user_surname,
            'description': description,
            'is_issued': is_issued,
            'is_written_off': is_written_off
        }

        op.get_bind().execute(
            text('''
                DELETE FROM material_operations
                WHERE medical_material_id = (
                    SELECT id
                    FROM medical_materials
                    WHERE name = :material_name
                )
                AND department_id = (
                    SELECT id
                    FROM departments
                    WHERE name = :department_name
                )
                AND quantity = :quantity
                AND document_number = :document_number
                AND current_user_id = (
                    SELECT id
                    FROM users
                    WHERE surname = :user_surname
                )
                AND description = :description
                AND is_issued = :is_issued
                AND is_written_off = :is_written_off;
            '''),
            params
        )
