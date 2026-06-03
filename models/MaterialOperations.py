from app import db_connection

db = db_connection


class MaterialOperations(db.Model):
    __tablename__ = 'material_operations'

    id = db.Column(db.Integer, primary_key=True)
    medical_material_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    document_number = db.Column(db.String())
    department_id = db.Column(db.Integer())
    current_user_id = db.Column(db.Integer)
    operation_date = db.Column(db.DateTime())
    description = db.Column(db.String())
    is_issued = db.Column(db.Boolean)
    is_written_off = db.Column(db.Boolean)

    def __init__(self,
                 medical_material_id,
                 quantity,
                 document_number,
                 department_id,
                 current_user_id,
                 operation_date,
                 description,
                 is_issued=False,
                 is_written_off=False):
        self.medical_material_id = medical_material_id
        self.quantity = quantity
        self.document_number = document_number
        self.department_id = department_id
        self.current_user_id = current_user_id
        self.operation_date = operation_date
        self.description = description
        self.is_issued = is_issued
        self.is_written_off = is_written_off
        