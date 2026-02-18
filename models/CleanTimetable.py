from app import db_connection

db = db_connection


class CleanTimetable(db.Model):
    __tablename__ = 'clean_timetable'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    clean_datetime = db.Column(db.DateTime())

    def __init__(self, user_id, room_id, clean_datetime):
        self.user_id = user_id
        self.room_id = room_id
        self.clean_datetime = clean_datetime

    def __json__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "clean_datetime": self.clean_datetime
        }

    def __repr__(self):
        return f"<CleanTimetable {self.id}>"
