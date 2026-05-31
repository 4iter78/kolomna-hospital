from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.RoomType import RoomType
from app import db_connection
from decorators import access_control

db = db_connection
room_type_controller = Blueprint('room_type_controller', __name__)


@room_type_controller.route('/room_type', methods=['POST', 'GET'])
@access_control('room_type')
def handle_room_types():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_room_type = RoomType(name=data['name'])
        db.session.add(new_room_type)
        db.session.commit()
        flash(f"Тип помещения {new_room_type.name} с идентификатором {new_room_type.id} успешно создан.",
              'success')
        return redirect(url_for('room_type_controller.handle_room_types'))

    elif request.method == 'GET':
        room_types = RoomType.query.all()
        results = [{"id": rt.id, "name": rt.name} for rt in room_types]
        return render_template('room_type.html', title='Типы помещений',
                               room_types=results, count=len(results))


@room_type_controller.route('/room_type/<room_type_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('room_type')
def handle_room_type(room_type_id):
    room_type = RoomType.query.get_or_404(room_type_id)

    if request.method == 'GET':
        return {"message": "success", "room_type": {"id": room_type.id, "name": room_type.name}}

    elif request.method == 'PUT':
        data = request.get_json()
        room_type.name = data['name']
        db.session.add(room_type)
        db.session.commit()
        return {"message": f"Тип помещения {room_type.name} успешно обновлен"}

    elif request.method == 'DELETE':
        db.session.delete(room_type)
        db.session.commit()
        return {"message": f"Тип помещения {room_type.name} успешно удален."}
