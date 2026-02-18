from app import db_connection

db = db_connection


class Rooms(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    room_type_id = db.Column(db.Integer)
    special_type_id = db.Column(db.Integer, nullable=True)

    def __init__(self, name, room_type_id, special_type_id=None):
        self.name = name
        self.room_type_id = room_type_id
        self.special_type_id = special_type_id

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "room_type_id": self.room_type_id,
            "special_type_id": self.special_type_id
        }

    def __repr__(self):
        return f"<Room {self.name}>"
