from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.WorkTimetable import WorkTimetable
from models.Rooms import Rooms
from app import db_connection

db = db_connection
work_timetable_controller = Blueprint('work_timetable_controller', __name__)


@work_timetable_controller.route('/work_timetable', methods=['POST', 'GET'])
def handle_work_timetables():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_entry = WorkTimetable(
                room_id=data['room_id'],
                work_date=data['work_date'],
                time_from=data['time_from'],
                time_to=data['time_to']
            )
            db.session.add(new_entry)
            db.session.commit()
            flash(f"Рабочее расписание с идентификатором {new_entry.id} успешно создано.",
                  'success')
            return redirect(url_for('work_timetable_controller.handle_work_timetables'))
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        entries = WorkTimetable.query.all()
        results = []
        for e in entries:
            room = Rooms.query.get(e.room_id) if e.room_id else None
            results.append({
                "id": e.id,
                "room_id": e.room_id,
                "room": room.name if room else '',
                "work_date": e.work_date,
                "time_from": e.time_from,
                "time_to": e.time_to
            })
        return render_template('work_timetable.html', title='Расписание работы',
                               work_timetable=results, count=len(results))


@work_timetable_controller.route('/work_timetable/<entry_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_work_timetable(entry_id):
    entry = WorkTimetable.query.get_or_404(entry_id)

    if request.method == 'GET':
        room = Rooms.query.get(entry.room_id) if entry.room_id else None
        response = {
            "id": entry.id,
            "room": room.name if room else '',
            "work_date": entry.work_date,
            "time_from": entry.time_from,
            "time_to": entry.time_to
        }
        return {"message": "success", "work_timetable": response}

    elif request.method == 'PUT':
        data = request.get_json()
        entry.room_id = data['room_id']
        entry.work_date = data['work_date']
        entry.time_from = data['time_from']
        entry.time_to = data['time_to']
        db.session.add(entry)
        db.session.commit()
        return {"message": f"work_timetable {entry.id} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(entry)
        db.session.commit()
        return {"message": f"work_timetable {entry.id} successfully deleted."}
