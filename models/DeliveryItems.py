from app import db_connection

db = db_connection


class DeliveryItems(db.Model):
    __tablename__ = 'delivery_items'

    id = db.Column(db.Integer, primary_key=True)
    stock_delivery_id = db.Column(db.Integer)
    medical_material_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric())

    def __init__(self,
                 stock_delivery_id,
                 medical_material_id,
                 quantity,
                 unit_price):

        self.stock_delivery_id = stock_delivery_id
        self.medical_material_id = medical_material_id
        self.quantity = quantity
        self.unit_price = unit_price
        