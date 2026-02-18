from app import db_connection

db = db_connection


class Patients(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String())
    name = db.Column(db.String())
    second_name = db.Column(db.String())
    birth_date = db.Column(db.Date())
    birth_place = db.Column(db.String())
    phone = db.Column(db.String())
    email = db.Column(db.String())
    address = db.Column(db.Text())
    passport = db.Column(db.String())
    oms_number = db.Column(db.String())

    def __init__(self, surname, name, second_name, birth_date, birth_place,
                 phone, email, address, passport, oms_number):
        self.surname = surname
        self.name = name
        self.second_name = second_name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.phone = phone
        self.email = email
        self.address = address
        self.passport = passport
        self.oms_number = oms_number

    def __json__(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "second_name": self.second_name,
            "birth_date": self.birth_date,
            "birth_place": self.birth_place,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "passport": self.passport,
            "oms_number": self.oms_number
        }

    def __repr__(self):
        return f"<Patient {self.surname} {self.name} {self.second_name}>"
