from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.Departments import Departments
from app import db_connection
from decorators import access_control

db = db_connection
department_controller = Blueprint('department_controller', __name__)


@department_controller.route('/departments', methods=['POST', 'GET'])
@access_control('departments')
def handle_departments():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            new_department = Departments(name=data['name'])
            db.session.add(new_department)
            db.session.commit()
            flash(f"Отделение {new_department.name} с идентификатором {new_department.id} "
                  f"успешно создано.", 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"{str(e)}", "danger")
        return redirect(url_for('department_controller.handle_departments'))

    elif request.method == 'GET':
        departments = Departments.query.all()
        results = [{"id": rt.id, "name": rt.name} for rt in departments]
        return render_template('departments.html', title='Отделения',
                               departments=results, count=len(results))


@department_controller.route('/departments/<department_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('departments')
def handle_department(department_id):
    department = Departments.query.get_or_404(department_id)

    if request.method == 'GET':
        return {"message": "success", "department": {"id": department.id, "name": department.name}}

    elif request.method == 'PUT':
        data = request.get_json()
        department.name = data['name']
        db.session.add(department)
        db.session.commit()
        return {"message": f"Отделение {department.name} успешно обновлено"}

    elif request.method == 'DELETE':
        db.session.delete(department)
        db.session.commit()
        return {"message": f"Отделение {department.name} успешно удалено."}
