"""create function users

Revision ID: 17a3d50bae3f
Revises: f9fb52931c5e
Create Date: 2026-05-12 20:17:57.967093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '17a3d50bae3f'
down_revision: Union[str, Sequence[str], None] = 'f9fb52931c5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    -- Функция триггера для работы с паролем
    CREATE OR REPLACE FUNCTION trg_users_hash_password()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        -- Если поле password передано и не пустое — считаем хеш
        IF NEW.password IS NOT NULL AND NEW.password <> '' THEN
            NEW.hash_password := encode(digest(NEW.password, 'sha256'), 'hex');
        END IF;
        -- Очищаем password — значение не сохраняется в таблице
        NEW.password := NULL;
        RETURN NEW;
    END;
    $$;
    ''')


def downgrade() -> None:
    op.execute('''
    DROP FUNCTION IF EXISTS trg_users_hash_password();
    ''')
