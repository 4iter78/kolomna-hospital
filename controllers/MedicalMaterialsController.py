from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app import db_connection
from decorators import access_control
from models.MaterialTypes import MaterialTypes
from models.MaterialUnits import MaterialUnits
from models.MedicalMaterials import MedicalMaterials

db = db_connection

medical_materials_controller = Blueprint(
    'medical_materials_controller',
    __name__
)


@medical_materials_controller.route('/medical_materials', methods=['GET', 'POST'])
@access_control('medical_materials')
def handle_medical_materials():

    if request.method == 'POST':
        try:
            data = request.form
            material = MedicalMaterials(
                name=data['name'],
                material_type_id=data['material_type_id'],
                material_unit_id=data['material_unit_id'],
                description=data.get('description')
            )
            db.session.add(material)
            db.session.commit()
            flash(f'Материал "{material.name}" успешно создан','success')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f"Материал не может быть создан. {str(e)}", 'danger')
        return redirect(
            url_for(
                'medical_materials_controller.handle_medical_materials'
            )
        )

    elif request.method == 'GET':
        materials = MedicalMaterials.query.all()
        result = []
        for material in materials:
            material_type = MaterialTypes.query.get(
                material.material_type_id
            )
            material_unit = MaterialUnits.query.get(
                material.material_unit_id
            )
            result.append({
                "id":
                    material.id,
                "name":
                    material.name,
                "material_type_id":
                    material.material_type_id,
                "material_type":
                    material_type.name if material_type else '',
                "material_unit_id":
                    material.material_unit_id,
                "material_unit":
                    material_unit.name if material_unit else '',
                "description":
                    material.description
            })
        material_types = [
            {
                "id": item.id,
                "name": item.name
            }
            for item in MaterialTypes.query.all()
        ]
        material_units = [
            {
                "id": item.id,
                "name": item.name
            }
            for item in MaterialUnits.query.all()
        ]
        return render_template(
            'medical_materials.html',
            title='Медицинские материалы',
            medical_materials=result,
            material_types=material_types,
            material_units=material_units,
            count=len(result)
        )

@medical_materials_controller.route('/medical_materials/<material_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('medical_materials')
def handle_medical_material(material_id):

    material = MedicalMaterials.query.get_or_404(
        material_id
    )

    if request.method == 'GET':
        response = {
            "id":
                material.id,
            "name":
                material.name,
            "material_type_id":
                material.material_type_id,
            "material_unit_id":
                material.material_unit_id,
            "description":
                material.description
        }
        return {
            "message": "success",
            "material": response
        }

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            material.name = data['name']
            material.material_type_id = data[
                'material_type_id'
            ]
            material.material_unit_id = data[
                'material_unit_id'
            ]
            material.description = data.get(
                'description'
            )
            db.session.add(material)
            db.session.commit()
            return {"success": True, "message": f"Материал {material.id} успешно обновлен"}
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"success": False, "message": f"Материал {material.name} не может быть обновлен. {str(e)}"}, 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(material)
            db.session.commit()
            return {"success": True, "message": f"Материал {material.id} успешно удален"}
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"success": False, "message": f"Материал {material.name} не может быть удален. {str(e)}"}, 400
