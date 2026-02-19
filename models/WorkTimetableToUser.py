from app import db_connection

db = db_connection


class WorkTimetableToUser(db.Model):
    __tablename__ = 'work_timetable_to_user'

    id                = db.Column(db.Integer, primary_key=True)
    work_timetable_id = db.Column(db.Integer,
                                  db.ForeignKey('work_timetable.id', ondelete='CASCADE'),
                                  nullable=False)
    user_id           = db.Column(db.Integer,
                                  db.ForeignKey('users.id', ondelete='CASCADE'),
                                  nullable=False)

    def __repr__(self):
        return f'<WorkTimetableToUser wt={self.work_timetable_id} user={self.user_id}>'
