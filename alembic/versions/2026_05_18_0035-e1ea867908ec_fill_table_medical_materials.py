"""fill table medical_materials

Revision ID: e1ea867908ec
Revises: aa6a3814abe3
Create Date: 2026-05-18 00:35:58.268103

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e1ea867908ec'
down_revision: Union[str, Sequence[str], None] = 'aa6a3814abe3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO medical_materials (
            name,
            material_type_id,
            material_unit_id,
            description
        )
        VALUES
            (
                'Бинт стерильный',
                (SELECT id FROM material_types WHERE name = 'Перевязочные материалы'),
                (SELECT id FROM material_units WHERE short_name = 'шт'),
                'Бинт медицинский стерильный'
            ),
            (
                'Шприц 5 мл',
                (SELECT id FROM material_types WHERE name = 'Инъекционные материалы'),
                (SELECT id FROM material_units WHERE short_name = 'шт'),
                'Одноразовый шприц'
            ),
            (
                'Медицинские перчатки',
                (SELECT id FROM material_types WHERE name = 'Средства защиты'),
                (SELECT id FROM material_units WHERE short_name = 'пар'),
                'Латексные перчатки'
            ),
            (
                'Хлоргексидин',
                (SELECT id FROM material_types WHERE name = 'Антисептики'),
                (SELECT id FROM material_units WHERE short_name = 'мл'),
                'Антисептическое средство'
            ),
            (
                'Скальпель',
                (SELECT id FROM material_types WHERE name = 'Инструменты'),
                (SELECT id FROM material_units WHERE short_name = 'шт'),
                'Хирургический инструмент'
            ),
            (
                'Парацетамол',
                (SELECT id FROM material_types
                 WHERE name = 'Медицинские препараты'),
                (SELECT id FROM material_units
                 WHERE short_name = 'уп'),
                'Жаропонижающий препарат'
            ),
            (
                'Амоксициллин',
                (SELECT id FROM material_types
                 WHERE name = 'Медицинские препараты'),
                (SELECT id FROM material_units
                 WHERE short_name = 'уп'),
                'Антибиотик широкого спектра'
            ),
            (
                'Физраствор 0.9%',
                (SELECT id FROM material_types
                 WHERE name = 'Медицинские препараты'),
                (SELECT id FROM material_units
                 WHERE short_name = 'мл'),
                'Раствор натрия хлорида'
            ),
            (
                'Лидокаин',
                (SELECT id FROM material_types
                 WHERE name = 'Медицинские препараты'),
                (SELECT id FROM material_units
                 WHERE short_name = 'мл'),
                'Местный анестетик'
            );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM medical_materials
        WHERE name IN (
            'Бинт стерильный',
            'Шприц 5 мл',
            'Медицинские перчатки',
            'Хлоргексидин',
            'Скальпель',
            'Парацетамол',
            'Амоксициллин',
            'Физраствор 0.9%',
            'Лидокаин'
        );
    ''')
