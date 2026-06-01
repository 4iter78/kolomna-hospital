"""fill table role_permissions

Revision ID: d14eb6d75cb8
Revises: e03cf8af2302
Create Date: 2026-05-12 21:16:55.839246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'd14eb6d75cb8'
down_revision: Union[str, Sequence[str], None] = 'e03cf8af2302'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    WITH r AS (SELECT id, code FROM entities),
     ins(role_name, code, can_read, can_write, own_only) AS (VALUES
        -- Врач (1)
        ('Врач', 'patients',        TRUE, FALSE, FALSE),
        ('Врач', 'health_cards',    TRUE, TRUE,  FALSE),
        ('Врач', 'work_timetable',  TRUE, TRUE,  TRUE ),  -- только своё
        ('Врач', 'diagnosises',     TRUE, TRUE,  FALSE),
        ('Врач', 'drugs',           TRUE, TRUE,  FALSE),
        ('Врач', 'treatment_types', TRUE, TRUE,  FALSE),
        ('Врач', 'rooms',           TRUE, FALSE, FALSE),
        ('Врач', 'room_type',       TRUE, FALSE, FALSE),
        -- Регистратор (2)
        ('Регистратор', 'patients',        TRUE, TRUE,  FALSE),
        ('Регистратор', 'health_cards',    TRUE, FALSE, FALSE),
        ('Регистратор', 'work_timetable',  TRUE, FALSE, FALSE),
        ('Регистратор', 'diagnosises',     TRUE, FALSE, FALSE),
        ('Регистратор', 'drugs',           TRUE, FALSE, FALSE),
        ('Регистратор', 'treatment_types', TRUE, FALSE, FALSE),
        ('Регистратор', 'rooms',           TRUE, FALSE, FALSE),
        ('Регистратор', 'room_type',       TRUE, FALSE, FALSE),
        -- Работник ИТ (3)
        ('Работник ИТ', 'work_timetable',  TRUE, FALSE, FALSE),
        ('Работник ИТ', 'diagnosises',     TRUE, FALSE, FALSE),
        ('Работник ИТ', 'drugs',           TRUE, FALSE, FALSE),
        ('Работник ИТ', 'treatment_types', TRUE, FALSE, FALSE),
        ('Работник ИТ', 'rooms',           TRUE, TRUE,  FALSE),
        ('Работник ИТ', 'room_type',       TRUE, TRUE,  FALSE),
        -- Аспирант (4)
        ('Аспирант', 'patients',        TRUE, FALSE, FALSE),
        ('Аспирант', 'health_cards',    TRUE, FALSE, FALSE),
        ('Аспирант', 'work_timetable',  TRUE, TRUE,  TRUE ),  -- только своё
        ('Аспирант', 'diagnosises',     TRUE, TRUE,  FALSE),
        ('Аспирант', 'drugs',           TRUE, TRUE,  FALSE),
        ('Аспирант', 'treatment_types', TRUE, TRUE,  FALSE),
        ('Аспирант', 'rooms',           TRUE, FALSE, FALSE),
        ('Аспирант', 'room_type',       TRUE, FALSE, FALSE),
        -- Обслуживающий персонал (5)
        ('Обслуживающий персонал', 'work_timetable',  TRUE, TRUE,  TRUE ),  -- только своё
        ('Обслуживающий персонал', 'clean_timetable', TRUE, TRUE,  TRUE ),  -- только своё
        -- Гость (6) — только просмотр публичного
        ('Гость', 'diagnosises',     TRUE, FALSE, FALSE),
        ('Гость', 'drugs',           TRUE, FALSE, FALSE),
        ('Гость', 'treatment_types', TRUE, FALSE, FALSE),
        ('Гость', 'rooms',           TRUE, FALSE, FALSE),
        ('Гость', 'room_type',       TRUE, FALSE, FALSE),
        -- Администратор (7) — полный доступ ко всему
        ('Администратор', 'users',           TRUE, TRUE, FALSE),
        ('Администратор', 'user_roles',      TRUE, TRUE, FALSE),
        ('Администратор', 'patients',        TRUE, TRUE, FALSE),
        ('Администратор', 'health_cards',    TRUE, TRUE, FALSE),
        ('Администратор', 'work_timetable',  TRUE, TRUE, FALSE),
        ('Администратор', 'clean_timetable', TRUE, TRUE, FALSE),
        ('Администратор', 'diagnosises',     TRUE, TRUE, FALSE),
        ('Администратор', 'drugs',           TRUE, TRUE, FALSE),
        ('Администратор', 'treatment_types', TRUE, TRUE, FALSE),
        ('Администратор', 'rooms',           TRUE, TRUE, FALSE),
        ('Администратор', 'room_type',       TRUE, TRUE, FALSE)
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
        ('Врач', 'patients'),
        ('Врач', 'health_cards'),
        ('Врач', 'work_timetable'),
        ('Врач', 'diagnosises'),
        ('Врач', 'drugs'),
        ('Врач', 'treatment_types'),
        ('Врач', 'rooms'),
        ('Врач', 'room_type'),
        # Регистратор
        ('Регистратор', 'patients'),
        ('Регистратор', 'health_cards'),
        ('Регистратор', 'work_timetable'),
        ('Регистратор', 'diagnosises'),
        ('Регистратор', 'drugs'),
        ('Регистратор', 'treatment_types'),
        ('Регистратор', 'rooms'),
        ('Регистратор', 'room_type'),
        # Работник ИТ
        ('Работник ИТ', 'work_timetable'),
        ('Работник ИТ', 'diagnosises'),
        ('Работник ИТ', 'drugs'),
        ('Работник ИТ', 'treatment_types'),
        ('Работник ИТ', 'rooms'),
        ('Работник ИТ', 'room_type'),
        # Аспирант
        ('Аспирант', 'patients'),
        ('Аспирант', 'health_cards'),
        ('Аспирант', 'work_timetable'),
        ('Аспирант', 'diagnosises'),
        ('Аспирант', 'drugs'),
        ('Аспирант', 'treatment_types'),
        ('Аспирант', 'rooms'),
        ('Аспирант', 'room_type'),
        # Обслуживающий персонал
        ('Обслуживающий персонал', 'work_timetable'),
        ('Обслуживающий персонал', 'clean_timetable'),
        # Гость
        ('Гость', 'diagnosises'),
        ('Гость', 'drugs'),
        ('Гость', 'treatment_types'),
        ('Гость', 'rooms'),
        ('Гость', 'room_type'),
        # Администратор
        ('Администратор', 'users'),
        ('Администратор', 'user_roles'),
        ('Администратор', 'patients'),
        ('Администратор', 'health_cards'),
        ('Администратор', 'work_timetable'),
        ('Администратор', 'clean_timetable'),
        ('Администратор', 'diagnosises'),
        ('Администратор', 'drugs'),
        ('Администратор', 'treatment_types'),
        ('Администратор', 'rooms'),
        ('Администратор', 'room_type')
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
