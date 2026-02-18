from app import db_connection

db = db_connection


class Diagnosises(db.Model):
    __tablename__ = 'diagnosises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"<Diagnosis {self.name}>"
