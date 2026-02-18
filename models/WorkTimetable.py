from app import db_connection

db = db_connection


class WorkTimetable(db.Model):
    __tablename__ = 'work_timetable'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    work_date = db.Column(db.Date())
    time_from = db.Column(db.Time())
    time_to = db.Column(db.Time())

    def __init__(self, room_id, work_date, time_from, time_to):
        self.room_id = room_id
        self.work_date = work_date
        self.time_from = time_from
        self.time_to = time_to

    def __json__(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "work_date": self.work_date,
            "time_from": self.time_from,
            "time_to": self.time_to
        }

    def __repr__(self):
        return f"<WorkTimetable {self.id}>"
