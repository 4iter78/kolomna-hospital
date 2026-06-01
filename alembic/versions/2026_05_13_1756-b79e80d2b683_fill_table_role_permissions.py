"""fill table role_permissions

Revision ID: b79e80d2b683
Revises: 198fba9af071
Create Date: 2026-05-13 17:56:55.428444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'b79e80d2b683'
down_revision: Union[str, Sequence[str], None] = '198fba9af071'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        WITH r AS (SELECT id, code FROM entities),
             ins(role_name, code, can_read, can_write, own_only, sort_order) AS (VALUES
                -- Регистратор (может смотреть)
                ('Регистратор', 'appointments', TRUE, FALSE, FALSE, 1),
                -- Врач (видит только свои и редактирует)
                ('Врач', 'appointments', TRUE, TRUE, TRUE, 2),
                -- Админ (всё)
                ('Администратор', 'appointments', TRUE, TRUE, FALSE, 3)
            )
        INSERT INTO role_permissions (role_id, entity_id, can_read, can_write, own_only)
        SELECT
            (SELECT id FROM user_roles WHERE name = ins.role_name),
            r.id,
            ins.can_read,
            ins.can_write,
            ins.own_only
        FROM ins
        JOIN r ON r.code = ins.code
        ORDER BY ins.sort_order
        ON CONFLICT (role_id, entity_id) DO UPDATE
        SET
            can_read  = EXCLUDED.can_read,
            can_write = EXCLUDED.can_write,
            own_only  = EXCLUDED.own_only;
    ''')


def downgrade() -> None:
    # Полный список записей для удаления: (название роли, код сущности)
    records_to_delete = [
        # Регистратор (может смотреть)
        ('Регистратор', 'appointments'),
        # Врач (видит только свои и редактирует)
        ('Врач', 'appointments'),
        # Администратор (всё)
        ('Администратор', 'appointments')
    ]

    for record in records_to_delete:
        role_name, entity_code = record

        # Параметры для подстановки в SQL‑запрос
        params = {
            'role_name': role_name,
            'entity_code': entity_code
        }

        op.get_bind().execute(
            text('''
                DELETE FROM role_permissions
                WHERE role_id = (
                    SELECT id FROM user_roles
                    WHERE name = :role_name
                )
                AND entity_id = (
                    SELECT id FROM entities
                    WHERE code = :entity_code
                )
            '''),
            params
        )
