from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.TreatmentTypes import TreatmentTypes
from app import db_connection

db = db_connection
treatment_types_controller = Blueprint('treatment_types_controller', __name__)


@treatment_types_controller.route('/treatment_types', methods=['POST', 'GET'])
def handle_treatment_types():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_treatment_type = TreatmentTypes(name=data['name'])
            db.session.add(new_treatment_type)
            db.session.commit()
            flash(f"Тип лечения {new_treatment_type.name} с идентификатором {new_treatment_type.id} "
                  f"успешно создан.",
                  'success')
            return redirect(url_for('treatment_types_controller.handle_treatment_types'))
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        treatment_types = TreatmentTypes.query.all()
        results = [{"id": t.id, "name": t.name} for t in treatment_types]
        return render_template('treatment_types.html', title='Типы лечения',
                               treatment_types=results, count=len(results))


@treatment_types_controller.route('/treatment_types/<treatment_type_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_treatment_type(treatment_type_id):
    treatment_type = TreatmentTypes.query.get_or_404(treatment_type_id)

    if request.method == 'GET':
        return {"message": "success", "treatment_type": {"id": treatment_type.id, "name": treatment_type.name}}

    elif request.method == 'PUT':
        data = request.get_json()
        treatment_type.name = data['name']
        db.session.add(treatment_type)
        db.session.commit()
        return {"message": f"treatment_type {treatment_type.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(treatment_type)
        db.session.commit()
        return {"message": f"treatment_type {treatment_type.name} successfully deleted."}
