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
        try:
            data = request.get_json() if request.is_json else request.form
            new_supplier = Suppliers(
                             name=data['name'],
                             contact_person=data['contact_person'],
                             phone=data['phone'],
                             email=data['email'],
                             address=data['address'])
            db.session.add(new_supplier)
            db.session.commit()
            flash(f"Поставщик {new_supplier.name} с идентификатором "
                  f"{new_supplier.id} успешно создан.", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Поставщик не может быть создан. {str(e)}", "danger")
        return redirect(url_for('suppliers_controller.handle_suppliers'))

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
        return render_template('suppliers.html', title='Поставщики медицинских материалов',
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
            "name": supplier.name,
            "contact_person": supplier.contact_person,
            "phone": supplier.phone,
            "email": supplier.email,
            "address": supplier.address
        }
        return {"message": "success", "supplier": response}

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            supplier.name = data['name']
            supplier.contact_person = data['contact_person']
            supplier.phone = data['phone']
            supplier.email = data['email']
            supplier.address = data['address']
            db.session.add(supplier)
            db.session.commit()
            return {"success": True, "message": f"Поставщик {supplier.name} успешно обновлен"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Поставщик {supplier.name} не может быть обновлено. {str(e)}"}, 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(supplier)
            db.session.commit()
            return {"success": True, "message": f"Поставщик {supplier.name} успешно удален."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Поставщик {supplier.name} не может быть удалено. {str(e)}"}, 400
