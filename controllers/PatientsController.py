from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.Patients import Patients
from app import db_connection
from decorators import access_control

db = db_connection
patients_controller = Blueprint('patients_controller', __name__)


@patients_controller.route('/patients', methods=['POST', 'GET'])
@access_control('patients')
def handle_patients():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_patient = Patients(
            surname=data['surname'],
            name=data['name'],
            second_name=data.get('second_name'),
            birth_date=data['birth_date'],
            birth_place=data.get('birth_place'),
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            passport=data.get('passport'),
            oms_number=data.get('oms_number')
        )
        db.session.add(new_patient)
        db.session.commit()
        flash(f"Пациент {new_patient.surname} {new_patient.name} с идентификатором {new_patient.id} "
              f"успешно создан.",
              'success')
        return redirect(url_for('patients_controller.handle_patients'))

    elif request.method == 'GET':
        patients = Patients.query.all()
        results = []
        for p in patients:
            results.append({
                "id": p.id,
                "surname": p.surname,
                "name": p.name,
                "second_name": p.second_name,
                "fio": f'{p.surname} {p.name} {p.second_name or ""}',
                "birth_date": p.birth_date,
                "birth_place": p.birth_place,
                "phone": p.phone,
                "email": p.email,
                "address": p.address,
                "passport": p.passport,
                "oms_number": p.oms_number
            })
        return render_template('patients.html', title='Пациенты',
                               patients=results, count=len(results))


@patients_controller.route('/patients/<patient_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('patients')
def handle_patient(patient_id):
    patient = Patients.query.get_or_404(patient_id)

    if request.method == 'GET':
        response = {
            "id": patient.id,
            "surname": patient.surname,
            "name": patient.name,
            "second_name": patient.second_name,
            "birth_date": patient.birth_date,
            "birth_place": patient.birth_place,
            "phone": patient.phone,
            "email": patient.email,
            "address": patient.address,
            "passport": patient.passport,
            "oms_number": patient.oms_number
        }
        return {"message": "success", "patient": response}

    elif request.method == 'PUT':
        data = request.get_json()
        patient.surname = data['surname']
        patient.name = data['name']
        patient.second_name = data.get('second_name')
        patient.birth_date = data['birth_date']
        patient.birth_place = data.get('birth_place')
        patient.phone = data.get('phone')
        patient.email = data.get('email')
        patient.address = data.get('address')
        patient.passport = data.get('passport')
        patient.oms_number = data.get('oms_number')
        db.session.add(patient)
        db.session.commit()
        return {"message": f"Пациент {patient.surname} {patient.name} успешно обновлен"}

    elif request.method == 'DELETE':
        db.session.delete(patient)
        db.session.commit()
        return {"message": f"Пациент {patient.surname} {patient.name} успешно удален."}
