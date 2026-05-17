"""fill table material_types

Revision ID: cd04016f67af
Revises: ba776610b9b5
Create Date: 2026-05-18 00:31:16.828763

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cd04016f67af'
down_revision: Union[str, Sequence[str], None] = 'ba776610b9b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO material_types (name, description) VALUES
            ('Перевязочные материалы', 'Бинты, марля, вата'),
            ('Инструменты', 'Медицинские инструменты'),
            ('Антисептики', 'Средства дезинфекции'),
            ('Инъекционные материалы', 'Шприцы, иглы'),
            ('Средства защиты', 'Маски, перчатки, халаты'),
            ('Медицинские препараты',
            'Лекарственные средства, медикаменты, растворы и препараты');
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM material_types
        WHERE name IN (
            'Перевязочные материалы',
            'Инструменты',
            'Антисептики',
            'Инъекционные материалы',
            'Средства защиты',
            'Медицинские препараты'
        );
    ''')
