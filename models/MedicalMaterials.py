from app import db_connection

db = db_connection


# Класс для представления таблицы medical_materials
class MedicalMaterials(db.Model):

    __tablename__ = 'medical_materials'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String())

    material_type_id = db.Column(db.Integer)

    material_unit_id = db.Column(db.Integer)

    description = db.Column(db.String())

    def __init__(self,
                 name,
                 material_type_id,
                 material_unit_id,
                 description=None):

        self.name = name

        self.material_type_id = material_type_id

        self.material_unit_id = material_unit_id

        self.description = description

    def __json__(self):

        return {

            "id": self.id,

            "name": self.name,

            "material_type_id": self.material_type_id,

            "material_unit_id": self.material_unit_id,

            "description": self.description
        }

    def __repr__(self):

        return f"<MedicalMaterial {self.name}>"
    