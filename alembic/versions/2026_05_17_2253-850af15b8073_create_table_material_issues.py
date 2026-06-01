"""create table material_issues

Revision ID: 850af15b8073
Revises: 8f2cef6ade51
Create Date: 2026-05-17 22:53:02.914432

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '850af15b8073'
down_revision: Union[str, Sequence[str], None] = '8f2cef6ade51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE TABLE material_issues (
            id            SERIAL PRIMARY KEY,
            from_user_id       INT NOT NULL REFERENCES users(id),  -- кто выдал
            to_user_id       INT NOT NULL REFERENCES users(id),  -- кому выдал
            issue_date    TIMESTAMP NOT NULL DEFAULT NOW(),
            department_id    INT REFERENCES departments(id),
            notes         TEXT
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
        DROP TABLE IF EXISTS material_issues;
    ''')
