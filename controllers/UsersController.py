from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection
from models.Departments import Departments
from models.UserDepartments import UserDepartments
from models.UserRoles import UserRoles
from models.Users import Users
from decorators import access_control

db = db_connection
users_controller = Blueprint('users_controller', __name__)


# маршрут к пользователям, POST добавляет запись в таблицу, GET выводит все записи
@users_controller.route('/users', methods=['POST', 'GET'])
@access_control('users')
def handle_users():
    print(f'handle_users')
    if request.method == 'POST':
        print(f'method post in users')
        try:
            data = request.get_json() if request.is_json else request.form
            new_user = Users(surname=data['surname'],
                             name=data['name'],
                             second_name=data['second_name'],
                             employment_date=data['employment_date'],
                             user_role_id=data['user_role_id'])

            department_ids = data.getlist('department_ids[]')
            db.session.add(new_user)
            db.session.commit()
            for dep_id in department_ids:
                user_department = UserDepartments(user_id=new_user.id, department_id=dep_id)
                db.session.add(user_department)
                db.session.commit()
            flash(f"Пользователь {new_user.surname} {new_user.name} {new_user.second_name} с идентификатором "
                  f"{new_user.id} успешно создан.", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Пользователь не может быть создан. {str(e)}", "danger")
        return redirect(url_for('users_controller.handle_users'))

    elif request.method == 'GET':
        users = Users.query.all()
        results = []
        for user in users:
            user_role = None
            if user.user_role_id is not None:
                user_role = UserRoles.query.get(user.user_role_id)

            department_ids = [
                d.department_id for d in
                db.session.query(UserDepartments.department_id)
                .filter(UserDepartments.user_id == user.id)
                .all()
            ]
            user_departments = Departments.query.filter(Departments.id.in_(department_ids)).all()
            txt_user = {
                "id": user.id,
                "surname": user.surname,
                "name": user.name,
                "second_name": user.second_name,
                "fio": f'{user.surname} {user.name} {user.second_name}',
                "employment_date": user.employment_date,
                "user_role_id": user.user_role_id,
                "user_role": user_role.name if user_role is not None else '',
                "department_ids": department_ids,
                "department":
                    ", ".join(department.name for department in user_departments if department.name)
            }
            results.append(txt_user)
        roles = [{"id": r.id, "name": r.name} for r in UserRoles.query.all()]
        departments = [
            {
                "id": department.id,
                "name": department.name
            }
            for department in Departments.query.all()
        ]
        return render_template('users.html', title='Пользователи',
                               users=results, user_roles=roles, departments=departments, count=len(results))


# маршрут к конкретному пользователю по его user_id
# GET выводит данные по конкретному пользователю
# PUT редактирует данные конкретного пользователя
# DELETE удаляет конкретного пользователя
@users_controller.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('users')
def handle_user(user_id):
    user = Users.query.get_or_404(user_id)

    if request.method == 'GET':
        user_role = None
        if user.user_role_id is not None:
            user_role = UserRoles.query.get(user.user_role_id)
        department_ids = [
            d.department_id for d in
            db.session.query(UserDepartments.department_id)
            .filter(UserDepartments.user_id == user.id)
            .all()
        ]
        departments = Departments.query.filter(
            Departments.id.in_(department_ids)
        ).all()
        response = {
            "id": user.id,
            "surname": user.surname,
            "name": user.name,
            "second_name": user.second_name,
            "employment_date": user.employment_date,
            "user_role": user_role.name if user_role is not None else '',
            "department_ids": department_ids,
            "department":
                ", ".join(department.name for department in departments if department.name)
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            user.surname = data['surname']
            user.name = data['name']
            user.second_name = data['second_name']
            user.employment_date = data['employment_date']
            user.user_role_id = data['user_role_id']
            department_ids = data["department_ids"]
            UserDepartments.query.filter_by(user_id=user.id).delete()
            for dep_id in department_ids:
                user_department = UserDepartments(user_id=user.id, department_id=dep_id)
                db.session.add(user_department)
            db.session.commit()
            return {"success": True, "message": f"Пользователь {user.surname} {user.name} {user.second_name} "
                                                f"успешно обновлен"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Пользователь {user.surname} {user.name} {user.second_name} "
                                                 f"не может быть обновлен. {str(e)}"}, 400

    elif request.method == 'DELETE':
        try:
            UserDepartments.query.filter_by(user_id=user.id).delete()
            db.session.delete(user)
            db.session.commit()
            return {"success": True, "message": f"Пользователь {user.surname} {user.name} {user.second_name} "
                                                f"успешно удален."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Пользователь {user.surname} {user.name} {user.second_name} "
                                                 f"не может быть удален. {str(e)}"}, 400
