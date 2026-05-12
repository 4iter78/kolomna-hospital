"""create trigger users

Revision ID: 17a3d50bae3f
Revises: f9fb52931c5e
Create Date: 2026-05-12 20:22:59.182944

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '17a3d50bae3f'
down_revision: Union[str, Sequence[str], None] = 'f9fb52931c5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE TRIGGER trg_users_hash_password
    BEFORE INSERT OR UPDATE OF password
    ON users
    FOR EACH ROW
    EXECUTE FUNCTION trg_users_hash_password();
    ''')


def downgrade() -> None:
    op.execute('''
    DROP TRIGGER IF EXISTS trg_users_hash_password ON users;
    ''')
