"""fill table role_permissions

Revision ID: 129d06c5471f
Revises: efd60a1f2c25
Create Date: 2026-05-18 04:37:55.964481

"""
from typing import Sequence, Union

from sqlalchemy import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '129d06c5471f'
down_revision: Union[str, Sequence[str], None] = 'efd60a1f2c25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        WITH r AS (SELECT id, code FROM entities),
            ins(role_name, code, can_read, can_write, own_only) AS (VALUES
                ('Врач', 'storage', TRUE, TRUE, TRUE),
                ('Врач', 'issued', TRUE, TRUE, TRUE),
                ('Провизор', 'storage', TRUE, TRUE, TRUE),
                ('Провизор', 'issued', TRUE, TRUE, TRUE),
                ('Провизор', 'written_off', TRUE, TRUE, TRUE),
                ('Медсестра', 'storage', TRUE, TRUE, TRUE),
                ('Медсестра', 'issued', TRUE, TRUE, TRUE),
                ('Медсестра', 'written_off', TRUE, TRUE, TRUE),
                ('Фельдшер', 'storage', TRUE, TRUE, TRUE),
                ('Фельдшер', 'issued', TRUE, TRUE, TRUE),
                ('Фельдшер', 'written_off', TRUE, TRUE, TRUE),
                ('Кладовщик', 'suppliers', TRUE, TRUE, FALSE),
                ('Кладовщик', 'delivery', TRUE, TRUE, FALSE),
                ('Кладовщик', 'issue', TRUE, TRUE, FALSE),
                ('Кладовщик', 'storage', TRUE, TRUE, TRUE),
                ('Кладовщик', 'written_off', TRUE, TRUE, TRUE),
                ('Кладовщик', 'material_types', TRUE, TRUE, TRUE),
                ('Кладовщик', 'material_units', TRUE, TRUE, TRUE),
                ('Администратор', 'suppliers', TRUE, TRUE, FALSE),
                ('Администратор', 'delivery', TRUE, TRUE, FALSE),
                ('Администратор', 'issue', TRUE, TRUE, FALSE),
                ('Администратор', 'storage', TRUE, TRUE, FALSE),
                ('Администратор', 'issued', TRUE, TRUE, FALSE),
                ('Администратор', 'written_off', TRUE, TRUE, FALSE),
                ('Администратор', 'material_types', TRUE, TRUE, FALSE),
                ('Администратор', 'material_units', TRUE, TRUE, FALSE)
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
                ('Регистратор', 'departments', TRUE, TRUE, FALSE),
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
    # Полный список записей role_permissions для удаления:
    records_to_delete = [
        ('Врач', 'storage'),
        ('Врач', 'issued'),
        ('Провизор', 'storage'),
        ('Провизор', 'issued'),
        ('Провизор', 'written_off'),
        ('Медсестра', 'storage'),
        ('Медсестра', 'issued'),
        ('Медсестра', 'written_off'),
        ('Фельдшер', 'storage'),
        ('Фельдшер', 'issued'),
        ('Фельдшер', 'written_off'),
        ('Кладовщик', 'suppliers'),
        ('Кладовщик', 'delivery'),
        ('Кладовщик', 'issue'),
        ('Кладовщик', 'storage'),
        ('Кладовщик', 'written_off'),
        ('Кладовщик', 'material_types'),
        ('Кладовщик', 'material_units'),
        ('Администратор', 'suppliers'),
        ('Администратор', 'delivery'),
        ('Администратор', 'issue'),
        ('Администратор', 'storage'),
        ('Администратор', 'issued'),
        ('Администратор', 'written_off'),
        ('Администратор', 'material_types'),
        ('Администратор', 'material_units')
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
                    SELECT id
                    FROM user_roles
                    WHERE name = :role_name
                )
                AND entity_id = (
                    SELECT id
                    FROM entities
                    WHERE code = :entity_code
                );
            '''),
            params
        )

        op.execute('''
            DELETE FROM role_permissions where entity_id = (SELECT id FROM entities WHERE name = 'departments');
        ''')
