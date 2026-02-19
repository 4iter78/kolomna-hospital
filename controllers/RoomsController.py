from flask import redirect, url_for, flash, request, Blueprint, render_template
from models.Rooms import Rooms
from models.RoomType import RoomType
from app import db_connection
from decorators import access_control

db = db_connection
rooms_controller = Blueprint('rooms_controller', __name__)


@rooms_controller.route('/rooms', methods=['POST', 'GET'])
@access_control('rooms')
def handle_rooms():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        new_room = Rooms(
            name=data['name'],
            room_type_id=data['room_type_id'],
            special_type_id=data.get('special_type_id')
        )
        db.session.add(new_room)
        db.session.commit()
        flash(f"Помещение {new_room.name} с идентификатором {new_room.id} успешно создано.",
              'success')
        return redirect(url_for('rooms_controller.handle_rooms'))

    elif request.method == 'GET':
        rooms = Rooms.query.all()
        results = []
        for room in rooms:
            room_type = RoomType.query.get(room.room_type_id) if room.room_type_id else None
            results.append({
                "id": room.id,
                "name": room.name,
                "room_type_id": room.room_type_id,
                "room_type": room_type.name if room_type else '',
                "special_type_id": room.special_type_id
            })

        room_types_list = [{"id": rt.id, "name": rt.name} for rt in RoomType.query.all()]

        return render_template('rooms.html', title='Помещения',
                               rooms=results, count=len(results),
                               room_types=room_types_list)


@rooms_controller.route('/rooms/<room_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('rooms')
def handle_room(room_id):
    room = Rooms.query.get_or_404(room_id)

    if request.method == 'GET':
        room_type = RoomType.query.get(room.room_type_id) if room.room_type_id else None
        response = {
            "id": room.id,
            "name": room.name,
            "room_type": room_type.name if room_type else '',
            "special_type_id": room.special_type_id
        }
        return {"message": "success", "room": response}

    elif request.method == 'PUT':
        data = request.get_json()
        room.name = data['name']
        room.room_type_id = data['room_type_id']
        room.special_type_id = data.get('special_type_id')
        db.session.add(room)
        db.session.commit()
        return {"message": f"room {room.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(room)
        db.session.commit()
        return {"message": f"room {room.name} successfully deleted."}
