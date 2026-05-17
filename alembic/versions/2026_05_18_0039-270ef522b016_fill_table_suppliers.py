"""fill table suppliers

Revision ID: 270ef522b016
Revises: e1ea867908ec
Create Date: 2026-05-18 00:39:53.865664

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '270ef522b016'
down_revision: Union[str, Sequence[str], None] = 'e1ea867908ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO suppliers (
            name,
            contact_person,
            phone,
            email,
            address
        )
        VALUES
            (
                'МедСнаб',
                'Иванов Сергей',
                '+7-900-111-22-33',
                'info@medsnab.ru',
                'г. Москва, ул. Центральная, 10'
            ),
            (
                'ФармТорг',
                'Петров Алексей',
                '+7-900-444-55-66',
                'sales@pharmtorg.ru',
                'г. Санкт-Петербург, Невский пр., 20'
            );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM suppliers
        WHERE name IN (
            'МедСнаб',
            'ФармТорг'
        );
    ''')
