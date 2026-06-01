from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection
from decorators import access_control
from models.MaterialTypes import MaterialTypes

db = db_connection
material_types_controller = Blueprint('material_types_controller', __name__)


@material_types_controller.route('/material_types', methods=['POST', 'GET'])
@access_control('material_types')
def handle_material_types():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            new_material_type = MaterialTypes(name=data['name'])
            db.session.add(new_material_type)
            db.session.commit()
            flash(f"Тип материалов {new_material_type.name} с идентификатором "
                  f"{new_material_type.id} успешно создан.", 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"{str(e)}", "danger")
        return redirect(url_for('material_types_controller.handle_material_types'))

    elif request.method == 'GET':
        material_types = MaterialTypes.query.all()
        results = [{"id": rt.id, "name": rt.name} for rt in material_types]
        return render_template('material_types.html', title='Типы медицинских материалов',
                               material_types=results, count=len(results))


@material_types_controller.route('/material_types/<material_type_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('material_types')
def handle_material_type(material_types_id):
    material_type = MaterialTypes.query.get_or_404(material_types_id)

    if request.method == 'GET':
        return {"message": "success", "material_types": {"id": material_type.id, "name": material_type.name}}

    elif request.method == 'PUT':
        data = request.get_json()
        material_type.name = data['name']
        db.session.add(material_type)
        db.session.commit()
        return {"message": f"Тип материалов {material_type.name} успешно обновлен"}

    elif request.method == 'DELETE':
        db.session.delete(material_type)
        db.session.commit()
        return {"message": f"Тип материалов {material_type.name} успешно удален."}
