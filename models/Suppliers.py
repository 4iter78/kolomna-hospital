from app import db_connection

db = db_connection


# Класс для представления таблицы suppliers
class Suppliers(db.Model):

    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    contact_person = db.Column(db.String())
    phone = db.Column(db.String())
    email = db.Column(db.String())
    address = db.Column(db.String())

    def __init__(self, name, contact_person=None, phone=None, email=None, address=None):
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email
        self.address = address

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    def __repr__(self):
        return f"<Supplier {self.name}>"
