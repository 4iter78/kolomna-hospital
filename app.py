from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_connection = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # подключение к базе данных СУБД://имя_пользователя:пароль@IP-адрес:порт/имя_базы_данных
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:cfvfz78!@localhost:5432/kolomna_hospital"
    db_connection.init_app(app)
    return app


# def init_db(app):
#     global db_connection
#     db_connection = SQLAlchemy(app)
#
#
# def get_db():
#     return db_connection
