"""fill table role_permissions

Revision ID: 9dca9718e005
Revises: 0d5119448b33
Create Date: 2026-06-03 06:44:24.365668

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '9dca9718e005'
down_revision: Union[str, Sequence[str], None] = '0d5119448b33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    WITH r AS (SELECT id, code FROM entities),
     ins(role_name, code, can_read, can_write, own_only) AS (VALUES
            -- Администратор
            ('Администратор', 'users', TRUE, TRUE, FALSE),
            ('Администратор', 'user_roles', TRUE, TRUE, FALSE),
            ('Администратор', 'suppliers', TRUE, TRUE, FALSE),
            ('Администратор', 'delivery', TRUE, TRUE, FALSE),
            ('Администратор', 'issue', TRUE, TRUE, FALSE),
            ('Администратор', 'storage', TRUE, TRUE, FALSE),
            ('Администратор', 'issued', TRUE, TRUE, FALSE),
            ('Администратор', 'written_off', TRUE, TRUE, FALSE),
            ('Администратор', 'material_types', TRUE, TRUE, FALSE),
            ('Администратор', 'material_units', TRUE, TRUE, FALSE),
            ('Администратор', 'medical_materials', TRUE, TRUE, FALSE),
            ('Администратор', 'departments', TRUE, TRUE, FALSE),
        
            -- Кладовщик
            ('Кладовщик', 'suppliers', TRUE, TRUE, FALSE),
            ('Кладовщик', 'delivery', TRUE, TRUE, FALSE),
            ('Кладовщик', 'issue', TRUE, TRUE, FALSE),
            ('Кладовщик', 'storage', TRUE, TRUE, FALSE),
            ('Кладовщик', 'issued', TRUE, FALSE, FALSE),
            ('Кладовщик', 'written_off', TRUE, TRUE, FALSE),
            ('Кладовщик', 'material_types', TRUE, TRUE, FALSE),
            ('Кладовщик', 'material_units', TRUE, TRUE, FALSE),
            ('Кладовщик', 'medical_materials', TRUE, TRUE, FALSE),
            ('Кладовщик', 'departments', TRUE, FALSE, FALSE),
            ('Кладовщик', 'users', TRUE, FALSE, FALSE),
        
            -- Фельдшер
            ('Фельдшер', 'storage', TRUE, TRUE, FALSE),
            ('Фельдшер', 'issued', TRUE, TRUE, FALSE),
            ('Фельдшер', 'written_off', TRUE, TRUE, FALSE),
            ('Фельдшер', 'departments', TRUE, FALSE, FALSE),
            ('Фельдшер', 'users', TRUE, FALSE, FALSE),
            ('Фельдшер', 'issue', TRUE, FALSE, FALSE),
        
            -- Медсестра
            ('Медсестра', 'storage', TRUE, TRUE, FALSE),
            ('Медсестра', 'issued', TRUE, TRUE, FALSE),
            ('Медсестра', 'written_off', TRUE, TRUE, FALSE),
            ('Медсестра', 'departments', TRUE, FALSE, FALSE),
            ('Медсестра', 'users', TRUE, FALSE, FALSE),
            ('Медсестра', 'issue', TRUE, FALSE, FALSE),
        
            -- Провизор
            ('Провизор', 'storage', TRUE, TRUE, FALSE),
            ('Провизор', 'issued', TRUE, TRUE, FALSE),
            ('Провизор', 'written_off', TRUE, TRUE, FALSE),
            ('Провизор', 'departments', TRUE, FALSE, FALSE),
            ('Провизор', 'users', TRUE, FALSE, FALSE),
            ('Провизор', 'issue', TRUE, FALSE, FALSE),
        
            -- Врач
            ('Врач', 'storage', TRUE, TRUE, FALSE),
            ('Врач', 'issued', TRUE, TRUE, FALSE),
            ('Врач', 'departments', TRUE, FALSE, FALSE),
            ('Врач', 'users', TRUE, FALSE, FALSE),
            ('Врач', 'issue', TRUE, FALSE, FALSE),
            ('Врач', 'written_off', TRUE, TRUE, FALSE),
            ('Врач', 'medical_materials', TRUE, FALSE, FALSE),
        
            -- Гость
            ('Гость', 'departments', TRUE, FALSE, FALSE),
            ('Гость', 'users', TRUE, FALSE, FALSE)
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
    ON CONFLICT (role_id, entity_id) DO UPDATE
    SET
        can_read  = EXCLUDED.can_read,
        can_write = EXCLUDED.can_write,
        own_only  = EXCLUDED.own_only;
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM role_permissions;
    ''')
