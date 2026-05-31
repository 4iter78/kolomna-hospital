from app import db_connection

db = db_connection


class MaterialUnits(db.Model):
    __tablename__ = 'material_units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    short_name = db.Column(db.String())

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "short_name": self.short_name
        }

    def __repr__(self):
        return f"<MaterialUnit {self.name}>"
