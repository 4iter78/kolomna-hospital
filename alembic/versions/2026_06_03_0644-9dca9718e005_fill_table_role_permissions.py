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
        -- Врач
        ('Врач', 'storage', TRUE, TRUE, FALSE),
        ('Врач', 'issued', TRUE, TRUE, FALSE),
        -- Гость (6) — только просмотр публичного
        -- Провизор, Медсестра, Фельдшер
        ('Провизор', 'storage', TRUE, TRUE, FALSE),
        ('Провизор', 'issued', TRUE, TRUE, FALSE),
        ('Провизор', 'written_off', TRUE, TRUE, FALSE),
        ('Медсестра', 'storage', TRUE, TRUE, FALSE),
        ('Медсестра', 'issued', TRUE, TRUE, FALSE),
        ('Медсестра', 'written_off', TRUE, TRUE, FALSE),
        ('Фельдшер', 'storage', TRUE, TRUE, FALSE),
        ('Фельдшер', 'issued', TRUE, TRUE, FALSE),
        ('Фельдшер', 'written_off', TRUE, TRUE, FALSE),
        -- Кладовщик — работа со складом
        ('Кладовщик', 'suppliers', TRUE, TRUE, FALSE),
        ('Кладовщик', 'delivery', TRUE, TRUE, FALSE),
        ('Кладовщик', 'issue', TRUE, FALSE, FALSE),
        ('Кладовщик', 'storage', TRUE, TRUE, FALSE),
        ('Кладовщик', 'issued', TRUE, TRUE, FALSE),
        ('Кладовщик', 'written_off', TRUE, TRUE, FALSE),
        ('Кладовщик', 'material_types', TRUE, TRUE, FALSE),
        ('Кладовщик', 'material_units', TRUE, TRUE, FALSE),
        ('Кладовщик', 'medical_materials', TRUE, TRUE, FALSE),
        -- Администратор — полный доступ ко всему
        ('Администратор', 'suppliers', TRUE, TRUE, FALSE),
        ('Администратор', 'delivery', TRUE, TRUE, FALSE),
        ('Администратор', 'issue', TRUE, TRUE, FALSE),
        ('Администратор', 'storage', TRUE, TRUE, FALSE),
        ('Администратор', 'issued', TRUE, TRUE, FALSE),
        ('Администратор', 'written_off', TRUE, TRUE, FALSE),
        ('Администратор', 'material_types', TRUE, TRUE, FALSE),
        ('Администратор', 'material_units', TRUE, TRUE, FALSE),
        ('Администратор', 'medical_materials', TRUE, TRUE, FALSE),
        ('Администратор', 'users',           TRUE, TRUE, FALSE),
        ('Администратор', 'user_roles',      TRUE, TRUE, FALSE)
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
    
    INSERT INTO role_permissions (role_id, entity_id, can_read, can_write, own_only)
        SELECT
            ur.id,
            e.id,
            TRUE,
            FALSE,
            FALSE
        FROM user_roles ur
        CROSS JOIN entities e
        WHERE e.code = 'departments' AND ur.id 
        NOT IN (SELECT id FROM user_roles WHERE name IN ('Регистратор', 'Администратор'))
        ON CONFLICT (role_id, entity_id) DO UPDATE
        SET
            can_read  = EXCLUDED.can_read,
            can_write = EXCLUDED.can_write,
            own_only  = EXCLUDED.own_only;

        WITH r AS (SELECT id, code FROM entities),
            ins(role_name, code, can_read, can_write, own_only) AS (VALUES
                ('Администратор', 'departments', TRUE, TRUE, FALSE)
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
    # Полный список записей для удаления: (название роли, код сущности)
    records_to_delete = [
        # Врач
        ('Врач', 'storage'),
        ('Врач', 'issued'),
        # Гость
        # Провизор, Медсестра, Фельдшер
        ('Провизор', 'storage'),
        ('Провизор', 'issued'),
        ('Провизор', 'written_off'),
        ('Медсестра', 'storage'),
        ('Медсестра', 'issued'),
        ('Медсестра', 'written_off'),
        ('Фельдшер', 'storage'),
        ('Фельдшер', 'issued'),
        ('Фельдшер', 'written_off'),
        # Кладовщик
        ('Кладовщик', 'suppliers'),
        ('Кладовщик', 'delivery'),
        ('Кладовщик', 'issue'),
        ('Кладовщик', 'issued'),
        ('Кладовщик', 'storage'),
        ('Кладовщик', 'written_off'),
        ('Кладовщик', 'material_types'),
        ('Кладовщик', 'material_units'),
        ('Кладовщик', 'medical_materials'),
        # Администратор
        ('Администратор', 'users'),
        ('Администратор', 'user_roles'),
        ('Администратор', 'suppliers'),
        ('Администратор', 'delivery'),
        ('Администратор', 'issue'),
        ('Администратор', 'storage'),
        ('Администратор', 'issued'),
        ('Администратор', 'written_off'),
        ('Администратор', 'material_types'),
        ('Администратор', 'material_units'),
        ('Администратор', 'medical_materials')
    ]

    for record in records_to_delete:
        role_name, entity_code = record

        # Параметры для подстановки в SQL-запрос
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

    op.execute('''
                DELETE FROM role_permissions where entity_id = (SELECT id FROM entities WHERE name = 'departments');
            ''')
