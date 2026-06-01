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
from models.Departments import Departments
from models.MaterialBalances import MaterialBalances
from models.MaterialOperations import MaterialOperations
from models.MedicalMaterials import MedicalMaterials

db = db_connection

material_balances_controller = Blueprint(
    'material_balances_controller',
    __name__
)


@material_balances_controller.route('/storage',methods=['GET'])
@access_control('storage')
def handle_storage():

    balances = MaterialBalances.query.all()

    available = []

    for balance in balances:

        material = MedicalMaterials.query.get(
            balance.medical_material_id
        )

        department = Departments.query.get(
            balance.department_id
        )

        txt_balance = {
            "id": balance.id,
            "medical_material_id":
                balance.medical_material_id,
            "medical_material":
                material.name if material else '',
            "current_quantity":
                balance.current_quantity,
            "document_number":
                '',
            "department_id":
                balance.department_id,
            "department":
                department.name if department else '',
            "operation_date":
                datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "last_updated":
                balance.last_updated,
            "description":
                '',
            "is_not_storage":
                department.name != 'Склад'
        }

        available.append(txt_balance)

    materials = [
        {
            "id": material.id,
            "name": material.name
        }

        for material in MedicalMaterials.query.all()
    ]

    departments = [
        {
            "id": department.id,
            "name": department.name
        }

        for department in Departments.query.all()
    ]

    return render_template(
        'storage.html',
        title='Медицинские материалы в наличии',
        available=available,
        materials=materials,
        departments=departments,
        available_count=len(available)
    )


@material_balances_controller.route('/issued',methods=['GET'])
@access_control('issued')
def handle_issued():

    issued_operations = MaterialOperations.query.filter_by(
        is_issued=True
    ).all()

    issued = []

    for operation in issued_operations:

        material = MedicalMaterials.query.get(
            operation.medical_material_id
        )

        txt_operation = {
            "id": operation.id,
            "medical_material":
                material.name if material else '',
            "quantity": operation.quantity,
            "document_number":
                operation.document_number,
            "operation_date":
                operation.operation_date
        }

        issued.append(txt_operation)

    materials = [
        {
            "id": material.id,
            "name": material.name
        }

        for material in MedicalMaterials.query.all()
    ]

    return render_template(
        'issued.html',
        title='Выданные медицинские материалы',
        issued=issued,
        materials=materials,
        issued_count=len(issued)
    )

@material_balances_controller.route('/issued/<issued_id>',methods=['PUT'])
@access_control('issued')
def handle_issued_item(issued_id):
    print("in issued id")

    balance = MaterialBalances.query.get_or_404(
        issued_id
    )

    material = MedicalMaterials.query.get_or_404(
        balance.medical_material_id
    )

    if request.method == 'PUT':
        try:
            data = request.get_json()

            new_material_operation = MaterialOperations(
                medical_material_id=balance.medical_material_id,
                quantity=data['quantity'],
                document_number=data['document_number'],
                department_id=balance.department_id,
                current_user_id=session.get('user_id'),
                operation_date=data['operation_date'],
                description=data['description'],
                is_issued=True
            )
            db.session.add(new_material_operation)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return {f"{str(e)}", "danger"}

        return {
            "message": f"Материал #{material.name} успешно выдан."
        }

@material_balances_controller.route('/written_off/<written_off_id>',methods=['PUT'])
@access_control('written_off')
def handle_written_off_item(written_off_id):
    print("in written_off id")

    balance = MaterialBalances.query.get_or_404(
        written_off_id
    )
    print(balance)

    material = MedicalMaterials.query.get_or_404(
        balance.medical_material_id
    )
    print(material)

    if request.method == 'PUT':
        try:
            data = request.get_json()

            new_material_operation = MaterialOperations(
                medical_material_id=balance.medical_material_id,
                quantity=data['quantity'],
                document_number=data['document_number'],
                department_id=balance.department_id,
                current_user_id=session.get('user_id'),
                operation_date=data['operation_date'],
                description=data['description'],
                is_written_off=True
            )
            db.session.add(new_material_operation)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return {f"{str(e)}", "danger"}

        return {
            "message": f"Материал #{material.name} успешно списан."
        }


@material_balances_controller.route('/written_off',methods=['GET'])
@access_control('written_off')
def handle_written_off():

    written_off_operations = MaterialOperations.query.filter_by(
        is_written_off=True
    ).all()

    written_off = []

    for operation in written_off_operations:

        material = MedicalMaterials.query.get(
            operation.medical_material_id
        )

        txt_operation = {
            "id": operation.id,
            "medical_material":
                material.name if material else '',
            "quantity": operation.quantity,
            "document_number":
                operation.document_number,
            "operation_date":
                operation.operation_date
        }

        written_off.append(txt_operation)

    materials = [
        {
            "id": material.id,
            "name": material.name
        }

        for material in MedicalMaterials.query.all()
    ]

    return render_template(
        'written_off.html',
        title='Списанные медицинские материалы',
        written_off=written_off,
        materials=materials,
        written_off_count=len(written_off)
    )
