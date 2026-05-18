from app import db_connection

db = db_connection


class StockDeliveries(db.Model):
    __tablename__ = 'stock_deliveries'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer)
    delivery_date = db.Column(db.Date())
    document_number = db.Column(db.String())
    notes = db.Column(db.String())

    def __init__(self,
                 supplier_id,
                 delivery_date,
                 document_number,
                 notes=None):

        self.supplier_id = supplier_id
        self.delivery_date = delivery_date
        self.document_number = document_number
        self.notes = notes

    def __json__(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "delivery_date": self.delivery_date,
            "document_number": self.document_number,
            "notes": self.notes
        }
