from flask import Blueprint, render_template

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
            "medical_material":
                material.name if material else '',
            "current_quantity":
                balance.current_quantity,
            "department":
                department.name if department else '',
            "last_updated":
                balance.last_updated
        }

        available.append(txt_balance)

    return render_template(
        'storage.html',
        title='Медицинские материалы в наличии',
        available=available,
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

    return render_template(
        'issued.html',
        title='Выданные медицинские материалы',
        issued=issued,
        issued_count=len(issued)
    )


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

    return render_template(
        'written_off.html',
        title='Списанные медицинские материалы',
        written_off=written_off,
        written_off_count=len(written_off)
    )
