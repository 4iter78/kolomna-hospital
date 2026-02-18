from app import db_connection

db = db_connection


# Класс для представления таблицы users (пользователи)
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String())
    name = db.Column(db.String())
    second_name = db.Column(db.String())
    employment_date = db.Column(db.Date())
    user_role_id = db.Column(db.Integer)
    login = db.Column(db.String())
    password = db.Column(db.String())
    hash_password = db.Column(db.String())
    # user_role = db.relationship('UserRoles', back_populates='user', uselist=False, foreign_keys=[user_role_id])

    def __init__(self, surname, name, second_name, employment_date, user_role_id, login=None, password=None):
        self.surname = surname
        self.name = name
        self.second_name = second_name
        self.employment_date = employment_date
        self.user_role_id = user_role_id
        self.login = login
        self.password = password
        # self.user_role = user_role

    def __json__(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "second_name": self.second_name,
            "employment_date": self.employment_date,
            "user_role_id": self.user_role_id,
            "login": self.login
        }

    def __repr__(self):
        return f"<User {self.surname} {self.name} {self.second_name}>"
