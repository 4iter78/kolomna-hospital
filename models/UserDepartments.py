from app import db_connection

db = db_connection


# Класс для представления таблицы users (пользователи)
class UserDepartments(db.Model):
    __tablename__ = 'department_to_user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, department_id):
        self.user_id = user_id
        self.department_id = department_id

    def __json__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "department_id": self.department_id
        }

    def __repr__(self):
        return f"<User departments {self.id}>"
