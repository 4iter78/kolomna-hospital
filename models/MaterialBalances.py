from app import db_connection

db = db_connection


class MaterialBalances(db.Model):
    __tablename__ = 'material_balances'

    id = db.Column(db.Integer, primary_key=True)
    medical_material_id = db.Column(db.Integer)
    current_quantity = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime())
    department_id = db.Column(db.Integer)

    def __init__(self,
                 medical_material_id,
                 current_quantity,
                 last_updated,
                 department_id):

        self.medical_material_id = medical_material_id
        self.current_quantity = current_quantity
        self.last_updated = last_updated
        self.department_id = department_id

    def __json__(self):
        return {
            "id": self.id,
            "medical_material_id": self.medical_material_id,
            "current_quantity": self.current_quantity,
            "last_updated": self.last_updated,
            "department_id": self.department_id
        }
    