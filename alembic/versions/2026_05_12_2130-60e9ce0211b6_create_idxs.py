"""create idxs

Revision ID: 60e9ce0211b6
Revises: d14eb6d75cb8
Create Date: 2026-05-12 21:30:46.938768

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '60e9ce0211b6'
down_revision: Union[str, Sequence[str], None] = 'd14eb6d75cb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    -- users
    CREATE INDEX idx_users_user_role_id ON users (user_role_id);
    -- health_cards
    CREATE INDEX idx_health_cards_patient_id ON health_cards (patient_id);
    CREATE INDEX idx_health_cards_user_id ON health_cards (user_id);
    -- appointments
    CREATE INDEX idx_appointments_user_id ON appointments (user_id);
    CREATE INDEX idx_appointments_health_card_id ON appointments (health_card_id);
    CREATE INDEX idx_appointments_treatment_type_id ON appointments (treatment_type_id);
    CREATE INDEX idx_appointments_diagnosis_id ON appointments (diagnosis_id);
    CREATE INDEX idx_appointments_datetime ON appointments (appointment_datetime);
    -- work_timetable
    CREATE INDEX idx_work_timetable_room_id ON work_timetable (room_id);
    CREATE INDEX idx_work_timetable_work_date ON work_timetable (work_date);
    -- clean_timetable
    CREATE INDEX idx_clean_timetable_user_id ON clean_timetable (user_id);
    CREATE INDEX idx_clean_timetable_room_id ON clean_timetable (room_id);
    CREATE INDEX idx_clean_timetable_datetime ON clean_timetable (clean_datetime);
    -- rooms
    CREATE INDEX idx_rooms_room_type_id ON rooms (room_type_id);
    CREATE INDEX idx_rooms_special_type_id ON rooms (special_type_id);
    -- training
    CREATE INDEX idx_training_special_type_id ON training (special_type_id);
    -- comments
    CREATE INDEX idx_comments_from_patient_id ON comments (from_patient_id);
    CREATE INDEX idx_comments_to_user_id ON comments (to_user_id);
    -- entities
    CREATE UNIQUE INDEX uq_entities_code ON entities (code);
    -- role_permissions
    CREATE INDEX idx_role_permissions_role_id ON role_permissions (role_id);
    CREATE INDEX idx_role_permissions_entity_id ON role_permissions (entity_id);
    CREATE UNIQUE INDEX uq_role_permissions_role_entity ON role_permissions (role_id, entity_id);
    -- drugs_to_appointment
    CREATE INDEX idx_drugs_to_appointment_drug_id ON drugs_to_appointment (drug_id);
    CREATE INDEX idx_drugs_to_appointment_appointment_id ON drugs_to_appointment (appointment_id);
    -- training_to_user
    CREATE INDEX idx_training_to_user_training_id ON training_to_user (training_id);
    CREATE INDEX idx_training_to_user_user_id ON training_to_user (user_id);
    -- room_to_user
    CREATE INDEX idx_room_to_user_room_id ON room_to_user (room_id);
    CREATE INDEX idx_room_to_user_user_id ON room_to_user (user_id);
    -- work_timetable_to_user
    CREATE INDEX idx_work_timetable_to_user_timetable_id ON work_timetable_to_user (work_timetable_id);
    CREATE INDEX idx_work_timetable_to_user_user_id ON work_timetable_to_user (user_id);
    -- request_to_user
    CREATE INDEX idx_request_to_user_request_id ON request_to_user (request_id);
    CREATE INDEX idx_request_to_user_user_id ON request_to_user (user_id);
    ''')
    pass


def downgrade() -> None:
    # users
    op.drop_index('idx_users_user_role_id', table_name='users')

    # health_cards
    op.drop_index('idx_health_cards_patient_id', table_name='health_cards')
    op.drop_index('idx_health_cards_user_id', table_name='health_cards')

    # appointments
    op.drop_index('idx_appointments_user_id', table_name='appointments')
    op.drop_index('idx_appointments_health_card_id', table_name='appointments')
    op.drop_index('idx_appointments_treatment_type_id', table_name='appointments')
    op.drop_index('idx_appointments_diagnosis_id', table_name='appointments')
    op.drop_index('idx_appointments_datetime', table_name='appointments')

    # work_timetable
    op.drop_index('idx_work_timetable_room_id', table_name='work_timetable')
    op.drop_index('idx_work_timetable_work_date', table_name='work_timetable')

    # clean_timetable
    op.drop_index('idx_clean_timetable_user_id', table_name='clean_timetable')
    op.drop_index('idx_clean_timetable_room_id', table_name='clean_timetable')
    op.drop_index('idx_clean_timetable_datetime', table_name='clean_timetable')

    # rooms
    op.drop_index('idx_rooms_room_type_id', table_name='rooms')
    op.drop_index('idx_rooms_special_type_id', table_name='rooms')

    # training
    op.drop_index('idx_training_special_type_id', table_name='training')

    # comments
    op.drop_index('idx_comments_from_patient_id', table_name='comments')
    op.drop_index('idx_comments_to_user_id', table_name='comments')

    # entities
    op.drop_index('uq_entities_code', table_name='entities')

    # role_permissions
    op.drop_index('idx_role_permissions_role_id', table_name='role_permissions')
    op.drop_index('idx_role_permissions_entity_id', table_name='role_permissions')
    op.drop_index('uq_role_permissions_role_entity', table_name='role_permissions')

    # drugs_to_appointment
    op.drop_index('idx_drugs_to_appointment_drug_id', table_name='drugs_to_appointment')
    op.drop_index('idx_drugs_to_appointment_appointment_id', table_name='drugs_to_appointment')

    # training_to_user
    op.drop_index('idx_training_to_user_training_id', table_name='training_to_user')
    op.drop_index('idx_training_to_user_user_id', table_name='training_to_user')

    # room_to_user
    op.drop_index('idx_room_to_user_room_id', table_name='room_to_user')
    op.drop_index('idx_room_to_user_user_id', table_name='room_to_user')

    # work_timetable_to_user
    op.drop_index('idx_work_timetable_to_user_timetable_id', table_name='work_timetable_to_user')
    op.drop_index('idx_work_timetable_to_user_user_id', table_name='work_timetable_to_user')

    # request_to_user
    op.drop_index('idx_request_to_user_request_id', table_name='request_to_user')
    op.drop_index('idx_request_to_user_user_id', table_name='request_to_user')
