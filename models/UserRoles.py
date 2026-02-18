from PP_2025.app import db_connection

db = db_connection


# Класс для представления таблицы users (пользователи)
class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # user = db.relationship('Users', back_populates='user_role')

    def __init__(self, name):
        self.name = name
        # self.user = user

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"<User role {self.name}>"

