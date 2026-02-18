from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.HealthCards import HealthCards
from models.Patients import Patients
from models.Users import Users
from app import db_connection
from datetime import datetime

db = db_connection
health_cards_controller = Blueprint('health_cards_controller', __name__)


@health_cards_controller.route('/health_cards', methods=['POST', 'GET'])
def handle_health_cards():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_health_card = HealthCards(
                patient_id=data['patient_id'],
                create_datetime=data.get('create_datetime', datetime.now()),
                user_id=data['user_id']
            )
            db.session.add(new_health_card)
            db.session.commit()
            flash(f"Медицинская карта с идентификатором {new_health_card.id} успешно создана.",
                  'success')
            return redirect(url_for('health_cards_controller.handle_health_cards'))
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        health_cards = HealthCards.query.all()
        results = []
        for hc in health_cards:
            patient = Patients.query.get(hc.patient_id) if hc.patient_id else None
            user = Users.query.get(hc.user_id) if hc.user_id else None
            results.append({
                "id": hc.id,
                "patient_id": hc.patient_id,
                "patient": f'{patient.surname} {patient.name} {patient.second_name or ""}' if patient else '',
                "create_datetime": hc.create_datetime,
                "user_id": hc.user_id,
                "user": f'{user.surname} {user.name} {user.second_name or ""}' if user else ''
            })
        return render_template('health_cards.html', title='Медицинские карты',
                               health_cards=results, count=len(results))


@health_cards_controller.route('/health_cards/<health_card_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_health_card(health_card_id):
    health_card = HealthCards.query.get_or_404(health_card_id)

    if request.method == 'GET':
        patient = Patients.query.get(health_card.patient_id) if health_card.patient_id else None
        user = Users.query.get(health_card.user_id) if health_card.user_id else None
        response = {
            "id": health_card.id,
            "patient_id": health_card.patient_id,
            "patient": f'{patient.surname} {patient.name}' if patient else '',
            "create_datetime": health_card.create_datetime,
            "user_id": health_card.user_id,
            "user": f'{user.surname} {user.name}' if user else ''
        }
        return {"message": "success", "health_card": response}

    elif request.method == 'PUT':
        data = request.get_json()
        health_card.patient_id = data['patient_id']
        health_card.create_datetime = data.get('create_datetime', health_card.create_datetime)
        health_card.user_id = data['user_id']
        db.session.add(health_card)
        db.session.commit()
        return {"message": f"health_card {health_card.id} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(health_card)
        db.session.commit()
        return {"message": f"health_card {health_card.id} successfully deleted."}
