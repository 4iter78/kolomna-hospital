from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app import db_connection

from decorators import access_control
from models.MaterialTypes import MaterialTypes
from models.MaterialUnits import MaterialUnits

from models.MaterialIssues import MaterialIssues
from models.IssueItems import IssueItems

from models.MedicalMaterials import MedicalMaterials
from models.Departments import Departments
from models.Users import Users

db = db_connection


material_issues_controller = Blueprint(
    'material_issues_controller',
    __name__
)


@material_issues_controller.route('/issue', methods=['GET', 'POST'])
@access_control('issue')
def handle_issue():

    if request.method == 'POST':
        try:
            data = request.form

            new_issue = MaterialIssues(
                from_user_id=data['from_user_id'],
                to_user_id=data['to_user_id'],
                department_id=data['department_id'],
                issue_date=data['issue_date'],
                notes=data['notes']
            )
            db.session.add(new_issue)
            db.session.commit()
            material_ids = request.form.getlist(
                'medical_material_id[]'
            )
            quantities = request.form.getlist(
                'quantity[]'
            )
            for i in range(len(material_ids)):
                item = IssueItems(
                    material_issue_id=new_issue.id,
                    medical_material_id=material_ids[i],
                    quantity=quantities[i]
                )
                db.session.add(item)
            db.session.commit()
            flash(f'Выдача #{new_issue.id} успешно создана.','success')
        except Exception as e:
            db.session.rollback()
            flash(f"Выдача не может быть создана. {str(e)}", "danger")
        return redirect(url_for('material_issues_controller.handle_issue'))

    elif request.method == 'GET':
        issues = MaterialIssues.query.all()
        result = []
        for issue in issues:
            from_user = Users.query.get(
                issue.from_user_id
            )
            to_user = Users.query.get(
                issue.to_user_id
            )
            department = Departments.query.get(
                issue.department_id
            )
            issue_items = IssueItems.query.filter_by(
                material_issue_id=issue.id
            ).all()
            items = []
            for item in issue_items:
                material = MedicalMaterials.query.get(
                    item.medical_material_id
                )
                material_type = None
                material_unit = None

                if material:
                    material_type = MaterialTypes.query.get(
                        material.material_type_id
                    )
                    material_unit = MaterialUnits.query.get(
                        material.material_unit_id
                    )
                txt_item = {
                    "id":
                        item.id,
                    "medical_material_id":
                        item.medical_material_id,
                    "medical_material":
                        material.name if material else '',
                    "material_type_id":
                        material.material_type_id if material else '',
                    "material_type":
                        material_type.name if material else '',
                    "material_unit_id":
                        material.material_unit_id if material else '',
                    "material_unit":
                        material_unit.short_name if material else '',
                    "quantity":
                        f'{item.quantity} {material_unit.short_name}' if material else ''
                }
                items.append(txt_item)
            txt_issue = {
                "id":
                    issue.id,
                "from_user_id":
                    issue.from_user_id,
                "to_user_id":
                    issue.to_user_id,
                "from_user": f'{from_user.surname} {from_user.name} {from_user.second_name}'
                if from_user else ''            ,
                "to_user": f'{to_user.surname} {to_user.name} {to_user.second_name}'
                if to_user else ''            ,
                "department_id":
                    issue.department_id,
                "department":
                    department.name if department else '',
                "issue_date":
                    issue.issue_date,
                "notes":
                    issue.notes,
                "issue_items":
                    items
            }
            result.append(txt_issue)
        users = [
            {
                "id": user.id,
                "surname": user.surname,
                "name": user.name,
                "second_name": user.second_name
            }
            for user in Users.query.all()
        ]
        departments = [
            {
                "id": department.id,
                "name": department.name
            }

            for department in Departments.query.all()
        ]
        materials = [
            {
                "id": material.id,
                "name": material.name,
                "material_type_id": material.material_type_id,
                "material_unit_id": material.material_unit_id
            }
            for material in MedicalMaterials.query.all()
        ]
        material_types = [
            {
                "id": material_type.id,
                "name": material_type.name
            }
            for material_type in MaterialTypes.query.all()
        ]
        material_units = [
            {
                "id": material_unit.id,
                "name": material_unit.short_name
            }
            for material_unit in MaterialUnits.query.all()
        ]
        current_user_id = session.get('user_id')
        today = datetime.now().strftime("%Y-%m-%dT%H:%M")
        return render_template(
            'issue.html',
            title='Выдача медицинских материалов со склада на отделение',
            issues=result,
            users=users,
            departments=departments,
            materials=materials,
            material_types=material_types,
            material_units=material_units,
            curr_user_id=current_user_id,
            today=today,
            count=len(result)
        )


@material_issues_controller.route('/issue/<issue_id>',methods=['GET', 'PUT', 'DELETE'])
@access_control('issue')
def handle_issue_item(issue_id):

    issue = MaterialIssues.query.get_or_404(
        issue_id
    )

    if request.method == 'GET':
        issue_items = IssueItems.query.filter_by(
            material_issue_id=issue.id
        ).all()
        print(f"issue items in GET {issue_items}")
        items = []
        for item in issue_items:
            material = MedicalMaterials.query.get(
                item.medical_material_id
            )
            material_type = None
            material_unit = None
            if material:
                material_type = MaterialTypes.query.get(
                    material.material_type_id
                )
                material_unit = MaterialUnits.query.get(
                    material.material_unit_id
                )
            txt_item = {
                "id":
                    item.id,
                "medical_material_id":
                    item.medical_material_id,
                "medical_material":
                    material.name if material else '',
                "material_type_id":
                    material.material_type_id if material else '',
                "material_type":
                    material_type.name if material else '',
                "material_unit_id":
                    material.material_unit_id if material else '',
                "material_unit":
                    material_unit.short_name if material else '',
                "quantity":
                    item.quantity
            }
            items.append(txt_item)
        response = {
            "id":
                issue.id,
            "from_user_id":
                issue.from_user_id,
            "to_user_id":
                issue.to_user_id,
            "department_id":
                issue.department_id,
            "issue_date":
                issue.issue_date,
            "notes":
                issue.notes,
            "issue_items":
                items
        }
        return {
            "message": "success",
            "issue": response
        }

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            issue.from_user_id = data[
                'from_user_id'
            ]
            issue.to_user_id = data[
                'to_user_id'
            ]
            issue.department_id = data[
                'department_id'
            ]
            issue.issue_date = data[
                'issue_date'
            ]
            issue.notes = data[
                'notes'
            ]
            db.session.add(issue)
            old_items = IssueItems.query.filter_by(
                material_issue_id=issue.id
            ).all()
            for item in old_items:
                db.session.delete(item)
            for item_data in data['issue_items']:
                db.session.add(
                    IssueItems(
                        material_issue_id=issue.id,
                        medical_material_id=item_data['medical_material_id'],
                        quantity=item_data['quantity' ]
                    )
                )
            db.session.commit()
            return {"success": True, "message": f"Выдача {issue.id} успешно обновлена"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Выдача {issue.id} не может быть обновлена. {str(e)}"}, 400

    elif request.method == 'DELETE':
        try:
            issue_items = IssueItems.query.filter_by(
                material_issue_id=issue.id
            ).all()
            for item in issue_items:
                db.session.delete(item)
            db.session.delete(issue)
            db.session.commit()
            return {"success": True, "message": f"Выдача {issue.id} успешно удалена"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Выдача {issue.name} не может быть удалена. {str(e)}"}, 400
