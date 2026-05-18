from app import db_connection

db = db_connection


class IssueItems(db.Model):
    __tablename__ = 'issue_items'

    id = db.Column(db.Integer, primary_key=True)
    material_issue_id = db.Column(db.Integer)
    medical_material_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self,
                 material_issue_id,
                 medical_material_id,
                 quantity):

        self.material_issue_id = material_issue_id
        self.medical_material_id = medical_material_id
        self.quantity = quantity
        