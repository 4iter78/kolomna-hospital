from flask import redirect, url_for, flash, request, Blueprint, render_template, session
from models.WorkTimetable import WorkTimetable
from models.WorkTimetableToUser import WorkTimetableToUser
from models.Rooms import Rooms
from app import db_connection
from decorators import access_control, access_control_with_ownership
from permissions import is_own_only

db = db_connection
work_timetable_controller = Blueprint('work_timetable_controller', __name__)


def _get_owner(entry_id):
    """Возвращает user_id владельца записи расписания."""
    link = WorkTimetableToUser.query.filter_by(
        work_timetable_id=entry_id
    ).first()
    return link.user_id if link else None


@work_timetable_controller.route('/work_timetable', methods=['POST', 'GET'])
@access_control('work_timetable')
def handle_work_timetables():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_entry = WorkTimetable(
            room_id=data['room_id'],
            work_date=data['work_date'],
            time_from=data['time_from'],
            time_to=data['time_to']
        )
        db.session.add(new_entry)
        db.session.commit()

        # Привязываем запись к текущему пользователю
        link = WorkTimetableToUser(
            work_timetable_id=new_entry.id,
            user_id=session.get('user_id')
        )
        db.session.add(link)
        db.session.commit()

        flash(f"Расписание с идентификатором {new_entry.id} успешно создано.", 'success')
        return redirect(url_for('work_timetable_controller.handle_work_timetables'))

    role    = session.get('user_role')
    user_id = session.get('user_id')

    # own_only берём из БД — не хардкод ролей
    if is_own_only('work_timetable', role):
        my_ids  = [r.work_timetable_id for r in
                   WorkTimetableToUser.query.filter_by(user_id=user_id).all()]
        entries = WorkTimetable.query.filter(WorkTimetable.id.in_(my_ids)).all()
    else:
        entries = WorkTimetable.query.all()

    results = []
    for e in entries:
        room  = Rooms.query.get(e.room_id) if e.room_id else None
        owner = WorkTimetableToUser.query.filter_by(
            work_timetable_id=e.id).first()
        results.append({
            "id":        e.id,
            "room_id":   e.room_id,
            "room":      room.name if room else '',
            "work_date": e.work_date,
            "time_from": e.time_from,
            "time_to":   e.time_to,
            "user_id":   owner.user_id if owner else None,  # для own_only в шаблоне
        })

    rooms_list = [{"id": r.id, "name": r.name} for r in Rooms.query.all()]
    return render_template('work_timetable.html', title='Расписание работы',
                           work_timetable=results, count=len(results),
                           rooms=rooms_list)


@work_timetable_controller.route('/work_timetable/<entry_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control_with_ownership('work_timetable', _get_owner)
def handle_work_timetable(entry_id):
    entry = WorkTimetable.query.get_or_404(entry_id)

    if request.method == 'GET':
        room = Rooms.query.get(entry.room_id) if entry.room_id else None
        return {"message": "success", "work_timetable": {
            "id":        entry.id,
            "room":      room.name if room else '',
            "work_date": entry.work_date,
            "time_from": entry.time_from,
            "time_to":   entry.time_to,
        }}

    elif request.method == 'PUT':
        data = request.get_json()
        entry.room_id   = data['room_id']
        entry.work_date = data['work_date']
        entry.time_from = data['time_from']
        entry.time_to   = data['time_to']
        db.session.add(entry)
        db.session.commit()
        return {"message": f"work_timetable {entry.id} successfully updated"}

    elif request.method == 'DELETE':
        # Сначала удаляем связь, потом саму запись
        WorkTimetableToUser.query.filter_by(
            work_timetable_id=entry.id).delete()
        db.session.delete(entry)
        db.session.commit()
        return {"message": f"work_timetable {entry.id} successfully deleted."}
