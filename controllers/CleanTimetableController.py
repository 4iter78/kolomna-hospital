from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.CleanTimetable import CleanTimetable
from models.Users import Users
from models.Rooms import Rooms
from app import db_connection
from decorators import access_control

db = db_connection
clean_timetable_controller = Blueprint('clean_timetable_controller', __name__)


@clean_timetable_controller.route('/clean_timetable', methods=['POST', 'GET'])
@access_control('clean_timetable')
def handle_clean_timetables():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            new_entry = CleanTimetable(
                user_id=data['user_id'],
                room_id=data['room_id'],
                clean_datetime=data['clean_datetime']
            )
            db.session.add(new_entry)
            db.session.commit()
            flash(f"Расписание уборки помещений с идентификатором {new_entry.id} успешно создано.",
              'success')

        except Exception as e:
            db.session.rollback()
            flash(f"{str(e)}", "danger")

        return redirect(url_for('clean_timetable_controller.handle_clean_timetables'))

    elif request.method == 'GET':
        entries = CleanTimetable.query.all()
        results = []
        for e in entries:
            user = Users.query.get(e.user_id) if e.user_id else None
            room = Rooms.query.get(e.room_id) if e.room_id else None
            results.append({
                "id": e.id,
                "user_id": e.user_id,
                "user": f'{user.surname} {user.name} {user.second_name or ""}' if user else '',
                "room_id": e.room_id,
                "room": room.name if room else '',
                "clean_datetime": e.clean_datetime
            })

        users_list = [
            {"id": u.id, "fio": f'{u.surname} {u.name} {u.second_name or ""}'}
            for u in Users.query.all()
        ]
        rooms_list = [{"id": r.id, "name": r.name} for r in Rooms.query.all()]

        return render_template('clean_timetable.html', title='Расписание уборки помещений',
                               clean_timetable=results, count=len(results),
                               users=users_list, rooms=rooms_list)


@clean_timetable_controller.route('/clean_timetable/<entry_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('clean_timetable')
def handle_clean_timetable(entry_id):
    entry = CleanTimetable.query.get_or_404(entry_id)

    if request.method == 'GET':
        user = Users.query.get(entry.user_id) if entry.user_id else None
        room = Rooms.query.get(entry.room_id) if entry.room_id else None
        response = {
            "id": entry.id,
            "user": f'{user.surname} {user.name}' if user else '',
            "room": room.name if room else '',
            "clean_datetime": entry.clean_datetime
        }
        return {"message": "success", "clean_timetable": response}

    elif request.method == 'PUT':
        data = request.get_json()
        entry.user_id = data['user_id']
        entry.room_id = data['room_id']
        entry.clean_datetime = data['clean_datetime']
        db.session.add(entry)
        db.session.commit()
        return {"message": f"Расписание {entry.id} успешно обновлено"}

    elif request.method == 'DELETE':
        db.session.delete(entry)
        db.session.commit()
        return {"message": f"Расписание {entry.id} успешно удалено."}
