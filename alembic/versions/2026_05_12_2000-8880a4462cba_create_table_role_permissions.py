"""create table role_permissions

Revision ID: 8880a4462cba
Revises: ef9965d241de
Create Date: 2026-05-12 20:00:58.166235

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8880a4462cba'
down_revision: Union[str, Sequence[str], None] = 'ef9965d241de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE TABLE IF NOT EXISTS role_permissions (
    id        SERIAL PRIMARY KEY,
    role_id   INTEGER REFERENCES user_roles(id) ON DELETE CASCADE,
    entity_id INTEGER REFERENCES entities(id)   ON DELETE CASCADE,
    can_read  BOOLEAN NOT NULL DEFAULT FALSE,
    can_write BOOLEAN NOT NULL DEFAULT FALSE,
    own_only  BOOLEAN NOT NULL DEFAULT FALSE,  -- только свои записи
    UNIQUE (role_id, entity_id)
    );
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS role_permissions;')
