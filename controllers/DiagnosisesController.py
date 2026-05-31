from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.Diagnosises import Diagnosises
from app import db_connection
from decorators import access_control

db = db_connection
diagnosises_controller = Blueprint('diagnosises_controller', __name__)


@diagnosises_controller.route('/diagnosises', methods=['POST', 'GET'])
@access_control('diagnosises')
def handle_diagnosises():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_diagnosis = Diagnosises(name=data['name'])
        db.session.add(new_diagnosis)
        db.session.commit()
        flash(f"Диагноз {new_diagnosis.name} с идентификатором {new_diagnosis.id} успешно создан.",
              'success')
        return redirect(url_for('diagnosises_controller.handle_diagnosises'))

    elif request.method == 'GET':
        diagnosises = Diagnosises.query.all()
        results = [{"id": d.id, "name": d.name} for d in diagnosises]
        return render_template('diagnosises.html', title='Диагнозы',
                               diagnosises=results, count=len(results))


@diagnosises_controller.route('/diagnosises/<diagnosis_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('diagnosises')
def handle_diagnosis(diagnosis_id):
    diagnosis = Diagnosises.query.get_or_404(diagnosis_id)

    if request.method == 'GET':
        return {"message": "success", "diagnosis": {"id": diagnosis.id, "name": diagnosis.name}}

    elif request.method == 'PUT':
        data = request.get_json()
        diagnosis.name = data['name']
        db.session.add(diagnosis)
        db.session.commit()
        return {"message": f"Диагноз {diagnosis.name} успешно обновлен"}

    elif request.method == 'DELETE':
        db.session.delete(diagnosis)
        db.session.commit()
        return {"message": f"Диагноз {diagnosis.name} успешно удален."}
