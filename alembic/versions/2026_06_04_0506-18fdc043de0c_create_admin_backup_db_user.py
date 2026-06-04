"""create admin_backup db user

Revision ID: 18fdc043de0c
Revises: 0770a5373493
Create Date: 2026-06-04 05:06:33.790072

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '18fdc043de0c'
down_revision: Union[str, Sequence[str], None] = '0770a5373493'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        -- Создание роли с правами на резервное копирование
        CREATE ROLE admin_backup WITH
            LOGIN
            PASSWORD 'xxxxxxx'
            REPLICATION;
        
        -- Права на подключение к базе данных
        GRANT CONNECT ON DATABASE kolomna_hospital TO admin_backup;
        
        -- Права на чтение всех таблиц (необходимо для pg_dump)
        GRANT USAGE ON SCHEMA public TO admin_backup;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO admin_backup;
        GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO admin_backup;
        
        -- Автоматически выдавать права на новые таблицы
        ALTER DEFAULT PRIVILEGES IN SCHEMA public
            GRANT SELECT ON TABLES TO admin_backup;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public
            GRANT SELECT ON SEQUENCES TO admin_backup;

    ''')


def downgrade():
    # Удаляем дефолтные привилегии
    op.execute("""
        ALTER DEFAULT PRIVILEGES IN SCHEMA public
            REVOKE SELECT ON TABLES FROM admin_backup;
    """)

    op.execute("""
        ALTER DEFAULT PRIVILEGES IN SCHEMA public
            REVOKE SELECT ON SEQUENCES FROM admin_backup;
    """)

    # Отзываем права на существующие объекты
    op.execute("""
        REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM admin_backup;
    """)

    op.execute("""
        REVOKE SELECT ON ALL SEQUENCES IN SCHEMA public FROM admin_backup;
    """)

    op.execute("""
        REVOKE USAGE ON SCHEMA public FROM admin_backup;
    """)

    op.execute("""
        REVOKE CONNECT ON DATABASE kolomna_hospital FROM admin_backup;
    """)

    # Удаляем роль
    op.execute("""
        REASSIGN OWNED BY admin_backup TO postgres;
        DROP OWNED BY admin_backup;
        DROP ROLE IF EXISTS admin_backup;
    """)
