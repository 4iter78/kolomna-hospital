from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.Appointments import Appointments
from models.Users import Users
from models.HealthCards import HealthCards
from models.Patients import Patients
from app import db_connection
from decorators import access_control
from datetime import datetime

db = db_connection
appointments_controller = Blueprint('appointments_controller', __name__)


# ───────────────────────────────────────────────
# LIST + CREATE
# ───────────────────────────────────────────────
@appointments_controller.route('/appointments', methods=['POST', 'GET'])
@access_control('appointments')
def handle_appointments():

    # ── CREATE ──────────────────────────────────
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        health_card = HealthCards.query.get({"patient_id": data.patient_id})

        new_appointment = Appointments(
            user_id=data['user_id'],
            health_card_id=health_card['id'],
            treatment_type_id=data['treatment_type_id'],
            appointment_datetime=data['appointment_datetime'],
            diagnosis_id=data['diagnosis_id']
        )

        db.session.add(new_appointment)
        db.session.commit()

        flash(f"Приём с идентификатором {new_appointment.id} успешно создан.", 'success')
        return redirect(url_for('appointments_controller.handle_appointments'))

    # ── GET ─────────────────────────────────────
    elif request.method == 'GET':
        appointments = Appointments.query.all()

        results = []
        for ap in appointments:
            user = Users.query.get(ap.user_id)
            health_card = HealthCards.query.get(ap.health_card_id)
            patient = Patients.query.get(health_card.patient_id)

            results.append({
                "id": ap.id,
                "user_id": ap.user_id,
                "user": f'{user.surname} {user.name} {user.second_name or ""}' if user else '',
                "health_card_id": ap.health_card_id,
                "patient_id": patient.id,
                "patient": f'{patient.surname} {patient.name} {patient.second_name or ""}' if patient else '',
                "appointment_datetime": ap.appointment_datetime,
                "treatment_type_id": ap.treatment_type_id,
                "diagnosis_id": ap.diagnosis_id
            })

        users_list = [
            {"id": u.id, "fio": f'{u.surname} {u.name} {u.second_name or ""}'}
            for u in Users.query.all()
        ]

        health_cards_list = [
            {"id": hc.id}
            for hc in HealthCards.query.all()
        ]

        patients_list = [
            {"id": p.id, "fio": f'{p.surname} {p.name} {p.second_name or ""}'}
            for p in Patients.query.all()
        ]

        return render_template(
            'appointments.html',
            title='Приёмы',
            appointments=results,
            count=len(results),
            users=users_list,
            health_cards=health_cards_list,
            patients_list=patients_list
        )


# ───────────────────────────────────────────────
# GET / UPDATE / DELETE
# ───────────────────────────────────────────────
@appointments_controller.route('/appointments/<appointment_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('appointments')
def handle_appointment(appointment_id):
    appointment = Appointments.query.get_or_404(appointment_id)

    # ── GET ─────────────────────────────────────
    if request.method == 'GET':
        return {
            "id": appointment.id,
            "user_id": appointment.user_id,
            "health_card_id": appointment.health_card_id,
            "treatment_type_id": appointment.treatment_type_id,
            "appointment_datetime": appointment.appointment_datetime.strftime('%Y-%m-%dT%H:%M') if appointment.appointment_datetime else '',
            "diagnosis_id": appointment.diagnosis_id
        }

    # ── UPDATE ──────────────────────────────────
    elif request.method == 'PUT':
        data = request.get_json()

        appointment.user_id = data['user_id']
        appointment.health_card_id = data['health_card_id']
        appointment.treatment_type_id = data.get('treatment_type_id')
        appointment.appointment_datetime = datetime.fromisoformat(data['appointment_datetime'])
        appointment.diagnosis_id = data.get('diagnosis_id')

        db.session.add(appointment)
        db.session.commit()

        return {"message": f"Приём {appointment.id} успешно обновлён"}

    # ── DELETE ──────────────────────────────────
    elif request.method == 'DELETE':
        db.session.delete(appointment)
        db.session.commit()

        return {"message": f"Приём {appointment.id} успешно удалён"}
