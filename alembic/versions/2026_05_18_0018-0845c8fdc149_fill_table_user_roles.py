"""fill table user_roles

Revision ID: 0845c8fdc149
Revises: 600be4f8fcc9
Create Date: 2026-05-18 00:18:12.478775

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0845c8fdc149'
down_revision: Union[str, Sequence[str], None] = '600be4f8fcc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        INSERT INTO user_roles (name) VALUES
            ('Провизор'),
            ('Кладовщик'),
            ('Медсестра'),
            ('Фельдшер');
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DELETE FROM user_roles WHERE name IN (
            'Провизор',
            'Кладовщик',
            'Медсестра',
            'Фельдшер');
    ''')
