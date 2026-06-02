from flask import Flask, session, redirect, url_for, request, render_template, send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from permissions import can_read, can_write, is_own_only
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
db_connection = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = '41be93f0a63b2584b7f01f638207b74b5208b5dfd6cb6133bff311335358ba1e'
    # подключение к базе данных СУБД://имя_пользователя:пароль@IP-адрес:порт/имя_базы_данных
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db_connection.init_app(app)

    # ── Получение иконки вкладки ────────────────────────────────
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    # ── Защита всех маршрутов ────────────────────────────────────
    @app.before_request
    def require_login():
        public_routes = ['auth_controller.login', 'static', 'favicon']
        if request.endpoint not in public_routes and not session.get('user_id'):
            return redirect(url_for('auth_controller.login', next=request.path))

    # ── Глобальные переменные прав для всех шаблонов ────────────
    @app.context_processor
    def inject_permissions():
        role    = session.get('user_role')
        user_id = session.get('user_id')

        return {
            'current_role':    role,
            'current_user_id': user_id,
            'can_read':    lambda entity: can_read(entity, role),
            'can_write':   lambda entity: can_write(entity, role),
            'is_own_only': lambda entity: is_own_only(entity, role),
        }

    # ── Страница 403 ─────────────────────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html', title='Доступ запрещён'), 403

    return app
