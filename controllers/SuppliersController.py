from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection
from decorators import access_control
from models.Suppliers import Suppliers

db = db_connection
suppliers_controller = Blueprint('suppliers_controller', __name__)


# маршрут к поставщикам, POST добавляет запись в таблицу, GET выводит все записи
@suppliers_controller.route('/suppliers', methods=['POST', 'GET'])
@access_control('suppliers')
def handle_suppliers():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_supplier = Suppliers(
                         name=data['name'],
                         contact_person=data['contact_person'],
                         phone=data['phone'],
                         email=data['email'],
                         address=data['address'])
        db.session.add(new_supplier)
        db.session.commit()
        flash(f"Поставщик {new_supplier.surname} {new_supplier.name} с идентификатором "
              f"{new_supplier.id} успешно создан.",
              'success')
        return redirect(url_for('users_controller.handle_users'))

    elif request.method == 'GET':
        suppliers = Suppliers.query.all()
        results = []
        for supplier in suppliers:
            txt_supplier = {
                "id": supplier.id,
                "name": supplier.name,
                "contact_person": supplier.contact_person,
                "phone": supplier.phone,
                "email": supplier.email,
                "address": supplier.address
            }
            results.append(txt_supplier)

        return render_template('suppliers.html', title='Поставщики',
                               suppliers=results, count=len(results))


# маршрут к конкретному поставщику по его supplier_id
# GET выводит данные по конкретному поставщику
# PUT редактирует данные конкретного поставщика
# DELETE удаляет конкретного поставщика
@suppliers_controller.route('/suppliers/<supplier_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('suppliers')
def handle_supplier(supplier_id):
    supplier = Suppliers.query.get_or_404(supplier_id)

    if request.method == 'GET':
        response = {
            "id": supplier.id,
            "surname": supplier.surname,
            "name": supplier.name,
            "second_name": supplier.second_name,
            "employment_date": supplier.employment_date
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        supplier.surname = data['surname']
        supplier.name = data['name']
        supplier.second_name = data['second_name']
        supplier.employment_date = data['employment_date']

        db.session.add(supplier)
        db.session.commit()

        return {"message": f"Поставщик {supplier.name} успешно обновлен"}

    elif request.method == 'DELETE':
        db.session.delete(supplier)
        db.session.commit()

        return {"message": f"Поставщик {supplier.surname} {supplier.name} {supplier.second_name} успешно удален."}
