from app import db_connection

db = db_connection


class Appointments(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # врач
    health_card_id = db.Column(db.Integer)
    treatment_type_id = db.Column(db.Integer)
    appointment_datetime = db.Column(db.DateTime())
    diagnosis_id = db.Column(db.Integer)

    def __init__(self, user_id, health_card_id, treatment_type_id, appointment_datetime, diagnosis_id=None):
        self.user_id = user_id
        self.health_card_id = health_card_id
        self.treatment_type_id = treatment_type_id
        self.appointment_datetime = appointment_datetime
        self.diagnosis_id = diagnosis_id

    def __repr__(self):
        return f"<Appointment {self.id}>"
