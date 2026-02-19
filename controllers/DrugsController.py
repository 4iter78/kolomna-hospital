from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.Drugs import Drugs
from app import db_connection
from decorators import access_control

db = db_connection
drugs_controller = Blueprint('drugs_controller', __name__)


@drugs_controller.route('/drugs', methods=['POST', 'GET'])
@access_control('drugs')
def handle_drugs():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_drug = Drugs(name=data['name'])
        db.session.add(new_drug)
        db.session.commit()
        flash(f"Препарат {new_drug.name} с идентификатором {new_drug.id} успешно создан.",
              'success')
        return redirect(url_for('drugs_controller.handle_drugs'))

    elif request.method == 'GET':
        drugs = Drugs.query.all()
        results = [{"id": d.id, "name": d.name} for d in drugs]
        return render_template('drugs.html', title='Препараты',
                               drugs=results, count=len(results))


@drugs_controller.route('/drugs/<drug_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('drugs')
def handle_drug(drug_id):
    drug = Drugs.query.get_or_404(drug_id)

    if request.method == 'GET':
        return {"message": "success", "drug": {"id": drug.id, "name": drug.name}}

    elif request.method == 'PUT':
        data = request.get_json()
        drug.name = data['name']
        db.session.add(drug)
        db.session.commit()
        return {"message": f"drug {drug.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(drug)
        db.session.commit()
        return {"message": f"drug {drug.name} successfully deleted."}
