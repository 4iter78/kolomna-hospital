from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection
from models.UserRoles import UserRoles
from decorators import access_control

db = db_connection
user_roles_controller = Blueprint('user_roles_controller', __name__)


# маршрут к пользователям, POST добавляет запись в таблицу, GET выводит все записи
@user_roles_controller.route('/user-roles', methods=['POST', 'GET'])
@access_control('user_roles')
def handle_user_roles():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            new_user_role = UserRoles(name=data['name'])
            db.session.add(new_user_role)
            db.session.commit()
            flash(f"Роль {new_user_role.name} с идентификатором {new_user_role.id} успешно создана.",
                  'success')
        except Exception as e:
            db.session.rollback()
            flash(f"{str(e)}", "danger")
        return redirect(url_for('user_roles_controller.handle_user_roles'))

    elif request.method == 'GET':
        user_roles = UserRoles.query.all()
        results = [
            {
                "id": user_role.id,
                "name": user_role.name
            } for user_role in user_roles]

        return render_template('roles.html', title='Роли пользователей',
                           user_roles=results, count=len(results))
        # {"count": len(results), "users": results}

# маршрут к конкретному пользователю по его user_id
# GET выводит данные по конкретному пользователю
# PUT редактирует данные конкретного пользователя
# DELETE удаляет конкретного пользователя
@user_roles_controller.route('/user-roles/<user_role_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('user_roles')
def handle_user_role(user_role_id):
    user_role = UserRoles.query.get_or_404(user_role_id)

    if request.method == 'GET':
        response = {
            "name": user_role.name,
        }
        return {"message": "success", "user_role": response}

    elif request.method == 'PUT':
        data = request.get_json()
        user_role.name = data['name']

        db.session.add(user_role)
        db.session.commit()

        return {"message": f"Роль {user_role.name} успешно обновлена"}

    elif request.method == 'DELETE':
        db.session.delete(user_role)
        db.session.commit()

        return {"message": f"Роль {user_role.name} успешно удалена."}
