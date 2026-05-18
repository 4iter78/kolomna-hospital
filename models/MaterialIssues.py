from app import db_connection

db = db_connection


class MaterialIssues(db.Model):
    __tablename__ = 'material_issues'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer)
    to_user_id = db.Column(db.Integer)
    issue_date = db.Column(db.DateTime())
    department_id = db.Column(db.Integer)
    notes = db.Column(db.String())

    def __init__(self,
                 from_user_id,
                 to_user_id,
                 issue_date,
                 department_id,
                 notes=None):

        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.issue_date = issue_date
        self.department_id = department_id
        self.notes = notes

    def __json__(self):
        return {
            "id": self.id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "issue_date": self.issue_date,
            "department_id": self.department_id,
            "notes": self.notes
        }
    