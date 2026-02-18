from app import db_connection

db = db_connection


class HealthCards(db.Model):
    __tablename__ = 'health_cards'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    create_datetime = db.Column(db.DateTime())
    user_id = db.Column(db.Integer)

    def __init__(self, patient_id, create_datetime, user_id):
        self.patient_id = patient_id
        self.create_datetime = create_datetime
        self.user_id = user_id

    def __json__(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "create_datetime": self.create_datetime,
            "user_id": self.user_id
        }

    def __repr__(self):
        return f"<HealthCard {self.id}>"
