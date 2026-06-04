from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection
from decorators import access_control
from models.MaterialUnits import MaterialUnits

db = db_connection
material_units_controller = Blueprint('material_units_controller', __name__)


@material_units_controller.route('/material_units', methods=['POST', 'GET'])
@access_control('material_units')
def handle_material_units():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            new_material_unit = MaterialUnits(name=data['name'], short_name=data['short_name'])
            db.session.add(new_material_unit)
            db.session.commit()
            flash(f"Единица измерения {new_material_unit.name} с идентификатором "
                  f"{new_material_unit.id} успешно создана.", 'success')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f"Единица измерения не может быть создана. {str(e)}", "danger")
        return redirect(url_for('material_units_controller.handle_material_units'))

    elif request.method == 'GET':
        material_units = MaterialUnits.query.all()
        results = [{"id": rt.id, "name": rt.name, "short_name": rt.short_name} for rt in material_units]
        return render_template('material_units.html',
                               title='Единицы измерения материалов',
                               material_units=results, count=len(results))


@material_units_controller.route('/material_units/<material_unit_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('material_units')
def handle_material_unit(material_units_id):
    material_unit = MaterialUnits.query.get_or_404(material_units_id)

    if request.method == 'GET':
        return {"message": "success", "material_units": {"id": material_unit.id, "name": material_unit.name}}

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            material_unit.name = data['name']
            material_unit.short_name = data['short_name']
            db.session.add(material_unit)
            db.session.commit()
            return {"success": True, "message": f"Единица измерения {material_unit.name} успешно обновлена"}
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"success": False, "message": f"Единица измерения {material_unit.name} не может быть обновлен. "
                                                 f"{str(e)}"}, 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(material_unit)
            db.session.commit()
            return {"success": True, "message": f"Единица измерения {material_unit.name} успешно удалена."}
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"success": False, "message": f"Единица измерения {material_unit.name} не может быть удален. "
                                                 f"{str(e)}"}, 400
