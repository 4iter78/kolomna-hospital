"""fill table issue_items

Revision ID: b43f943c21eb
Revises: 1f5ee4ca0aad
Create Date: 2026-05-18 01:02:03.935443

"""
from typing import Sequence, Union

from sqlalchemy import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b43f943c21eb'
down_revision: Union[str, Sequence[str], None] = '1f5ee4ca0aad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO issue_items (
            material_issue_id,
            medical_material_id,
            quantity
        )
        VALUES
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в приёмное отделение'),
                (SELECT id FROM medical_materials WHERE name = 'Бинт стерильный'),
                50
            ),
        
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в приёмное отделение'),
                (SELECT id FROM medical_materials WHERE name = 'Медицинские перчатки'),
                30
            ),
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в приёмное отделение'),
                (SELECT id FROM medical_materials WHERE name = 'Парацетамол'),
                20
            ),
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в приёмное отделение'),
                (SELECT id FROM medical_materials WHERE name = 'Физраствор 0.9%'),
                500
            ),
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в реанимацию'),
                (SELECT id FROM medical_materials WHERE name = 'Амоксициллин'),
                15
            ),
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в реанимацию'),
                (SELECT id FROM medical_materials WHERE name = 'Лидокаин'),
                100
            ),
            (
                (SELECT id FROM material_issues WHERE notes = 'Выдача в реанимацию'),
                (SELECT id FROM medical_materials WHERE name = 'Шприц 5 мл'),
                100
            );
    ''')


def downgrade() -> None:
    # Полный список записей issue_items для удаления:
    records_to_delete = [
        ('Выдача в приёмное отделение', 'Бинт стерильный', 50),
        ('Выдача в приёмное отделение', 'Медицинские перчатки', 30),
        ('Выдача в приёмное отделение', 'Парацетамол', 20),
        ('Выдача в приёмное отделение', 'Физраствор 0.9%', 500),
        ('Выдача в реанимацию', 'Амоксициллин', 15),
        ('Выдача в реанимацию', 'Лидокаин', 100),
        ('Выдача в реанимацию', 'Шприц 5 мл', 100),
    ]

    for record in records_to_delete:
        issue_notes, material_name, quantity = record

        # Параметры для подстановки в SQL-запрос
        params = {
            'issue_notes': issue_notes,
            'material_name': material_name,
            'quantity': quantity
        }

        op.get_bind().execute(
            text('''
                DELETE FROM issue_items
                WHERE material_issue_id = (
                    SELECT id
                    FROM material_issues
                    WHERE notes = :issue_notes
                )
                AND medical_material_id = (
                    SELECT id
                    FROM medical_materials
                    WHERE name = :material_name
                )
                AND quantity = :quantity
            '''),
            params
        )
