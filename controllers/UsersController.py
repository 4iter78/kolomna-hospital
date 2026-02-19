from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection
from models.UserRoles import UserRoles
from models.Users import Users

db = db_connection
users_controller = Blueprint('users_controller', __name__)


# маршрут к пользователям, POST добавляет запись в таблицу, GET выводит все записи
@users_controller.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_user = Users(surname=data['surname'],
                         name=data['name'],
                         second_name=data['second_name'],
                         employment_date=data['employment_date'],
                         user_role_id=data['user_role_id'])
        db.session.add(new_user)
        db.session.commit()
        flash(f"Пользователь {new_user.surname} {new_user.name} {new_user.second_name} с идентификатором "
              f"{new_user.id} успешно создан.",
              'success')
        return redirect(url_for('users_controller.handle_users'))

    elif request.method == 'GET':
        # db.session.query(Users, Profiles).join(Profiles, Users.id == Profiles.user_id).all()
        users = Users.query.all()
        results = []
        for user in users:
            user_role = None
            if user.user_role_id is not None:
                user_role = UserRoles.query.get(user.user_role_id)
            txt_user = {
                "id": user.id,
                "surname": user.surname,
                "name": user.name,
                "second_name": user.second_name,
                "fio": f'{user.surname} {user.name} {user.second_name}',
                "employment_date": user.employment_date,
                "user_role_id": user.user_role_id,
                "user_role": user_role.name if user_role is not None else ''
            }
            results.append(txt_user)

        roles = [{"id": r.id, "name": r.name} for r in UserRoles.query.all()]
        return render_template('users.html', title='Пользователи',
                               users=results, user_roles=roles, count=len(results))


# маршрут к конкретному пользователю по его user_id
# GET выводит данные по конкретному пользователю
# PUT редактирует данные конкретного пользователя
# DELETE удаляет конкретного пользователя
@users_controller.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user = Users.query.get_or_404(user_id)

    if request.method == 'GET':
        user_role = None
        if user.user_role_id is not None:
            user_role = UserRoles.query.get(user.user_role_id)
        response = {
            "id": user.id,
            "surname": user.surname,
            "name": user.name,
            "second_name": user.second_name,
            "employment_date": user.employment_date,
            "user_role": user_role.name if user_role is not None else ''
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        user.surname = data['surname']
        user.name = data['name']
        user.second_name = data['second_name']
        user.employment_date = data['employment_date']
        user.user_role_id = data['user_role_id']

        db.session.add(user)
        db.session.commit()

        return {"message": f"user {user.surname} {user.name} {user.second_name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return {"message": f"Customer {user.surname} {user.name} {user.second_name} successfully deleted."}
