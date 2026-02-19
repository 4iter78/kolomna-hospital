from flask import redirect, url_for, flash, request, Blueprint, render_template, session
from models.Users import Users
from app import db_connection

db = db_connection
auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.route('/login', methods=['GET', 'POST'])
def login():
    # Если уже авторизован — на главную
    if session.get('user_id'):
        return redirect(url_for('main_controller.index'))

    if request.method == 'POST':
        login_value = request.form.get('username', '').strip()
        password    = request.form.get('password', '').strip()

        if not login_value or not password:
            flash('Заполните все поля.', 'danger')
            return render_template('login.html')

        # Ищем по полю login
        user = Users.query.filter_by(login=login_value).first()

        # Проверяем хеш: передаём password через отдельный запрос к БД,
        # чтобы использовать ту же функцию pgcrypto что и триггер
        from sqlalchemy import text
        result = db.session.execute(
            text("SELECT encode(digest(:pwd, 'sha256'), 'hex') AS h"),
            {"pwd": password}
        ).fetchone()
        password_hash = result.h if result else None

        if user is None or user.hash_password != password_hash:
            flash('Неверный логин или пароль.', 'danger')
            return render_template('login.html')

        session['user_id']    = user.id
        session['user_name']  = f'{user.surname} {user.name}'
        session['user_login'] = user.login
        session['user_role']  = user.user_role_id
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main_controller.index'))

    return render_template('login.html')


@auth_controller.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('auth_controller.login'))
