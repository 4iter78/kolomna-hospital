"""fill table delivery_items

Revision ID: 02d6c24677a4
Revises: e75712ee9497
Create Date: 2026-05-18 00:44:40.322240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '02d6c24677a4'
down_revision: Union[str, Sequence[str], None] = 'e75712ee9497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO delivery_items (
            stock_delivery_id,
            medical_material_id,
            quantity,
            unit_price
        )
        VALUES
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'МедСнаб')),
                (SELECT id FROM medical_materials WHERE name = 'Бинт стерильный'),
                500,
                35.50
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'МедСнаб')),
                (SELECT id FROM medical_materials WHERE name = 'Шприц 5 мл'),
                1000,
                12.00
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'МедСнаб')),
                (SELECT id FROM medical_materials
                 WHERE name = 'Парацетамол'),
                200,
                45.00
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'МедСнаб')),
                (SELECT id FROM medical_materials
                 WHERE name = 'Амоксициллин'),
                150,
                120.00
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'ФармТорг')),
                (SELECT id FROM medical_materials
                 WHERE name = 'Физраствор 0.9%'),
                5000,
                0.80
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'ФармТорг')),
                (SELECT id FROM medical_materials
                 WHERE name = 'Лидокаин'),
                1000,
                1.50
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'ФармТорг')),
                (SELECT id FROM medical_materials WHERE name = 'Медицинские перчатки'),
                300,
                18.00
            ),
            (
                (SELECT id FROM stock_deliveries WHERE supplier_id = (SELECT id FROM suppliers WHERE name = 'ФармТорг')),
                (SELECT id FROM medical_materials WHERE name = 'Хлоргексидин'),
                2000,
                0.50
            );
    ''')
    pass


def downgrade() -> None:
    # Полный список записей delivery_items для удаления:
    records_to_delete = [
        ('МедСнаб', 'Бинт стерильный', 500, 35.50),
        ('МедСнаб', 'Шприц 5 мл', 1000, 12.00),
        ('МедСнаб', 'Парацетамол', 200, 45.00),
        ('МедСнаб', 'Амоксициллин', 150, 120.00),
        ('ФармТорг', 'Физраствор 0.9%', 5000, 0.80),
        ('ФармТорг', 'Лидокаин', 1000, 1.50),
        ('ФармТорг', 'Медицинские перчатки', 300, 18.00),
        ('ФармТорг', 'Хлоргексидин', 2000, 0.50),
    ]

    for record in records_to_delete:
        supplier_name, material_name, quantity, unit_price = record

        # Параметры для подстановки в SQL-запрос
        params = {
            'supplier_name': supplier_name,
            'material_name': material_name,
            'quantity': quantity,
            'unit_price': unit_price
        }

        op.get_bind().execute(
            text('''
                DELETE FROM delivery_items
                WHERE stock_delivery_id in (
                    SELECT id
                    FROM stock_deliveries
                    WHERE supplier_id = (
                        SELECT id
                        FROM suppliers
                        WHERE name = :supplier_name
                    )
                )
            '''),
            params
        )
