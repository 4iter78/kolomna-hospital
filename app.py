from flask import Flask, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

db_connection = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = '41be93f0a63b2584b7f01f638207b74b5208b5dfd6cb6133bff311335358ba1e'
    # подключение к базе данных СУБД://имя_пользователя:пароль@IP-адрес:порт/имя_базы_данных
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:cfvfz78!@localhost:5432/kolomna_hospital"
    db_connection.init_app(app)

    @app.before_request
    def require_login():
        public_routes = ['auth_controller.login', 'static']
        if request.endpoint not in public_routes and not session.get('user_id'):
            return redirect(url_for('auth_controller.login', next=request.path))

    return app


# def init_db(app):
#     global db_connection
#     db_connection = SQLAlchemy(app)
#
#
# def get_db():
#     return db_connection
