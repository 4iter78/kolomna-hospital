# ================================================================
# PermissionsController.py — страница матрицы прав (только для ADMIN)
# ================================================================

from flask import request, Blueprint, render_template, session, abort, jsonify
from models.Entities import Entities
from models.RolePermissions import RolePermissions
from models.UserRoles import UserRoles
from app import db_connection
from decorators import access_control

db = db_connection
permissions_controller = Blueprint('permissions_controller', __name__)


@permissions_controller.route('/admin/permissions', methods=['GET'])
@access_control('user_roles')  # только администратор имеет доступ к user_roles
def handle_permissions():
    roles    = UserRoles.query.order_by(UserRoles.id).all()
    entities = Entities.query.order_by(Entities.id).all()

    # Строим матрицу: { role_id: { entity_code: {can_read, can_write, own_only} } }
    matrix = {}
    for role in roles:
        matrix[role.id] = {}
        for entity in entities:
            perm = RolePermissions.query.filter_by(
                role_id=role.id, entity_id=entity.id
            ).first()
            matrix[role.id][entity.code] = {
                'can_read':  perm.can_read  if perm else False,
                'can_write': perm.can_write if perm else False,
                'own_only':  perm.own_only  if perm else False,
                'perm_id':   perm.id        if perm else None,
            }

    return render_template('permissions.html',
                           title='Матрица прав доступа',
                           roles=roles,
                           entities=entities,
                           matrix=matrix)


@permissions_controller.route('/admin/permissions/update', methods=['POST'])
@access_control('user_roles')
def update_permission():
    """
    Принимает JSON: { role_id, entity_id, field, value }
    field: 'can_read' | 'can_write' | 'own_only'
    Обновляет одну ячейку матрицы.
    """
    data      = request.get_json()
    role_id   = int(data['role_id'])
    entity_id = int(data['entity_id'])
    field     = data['field']    # 'can_read' | 'can_write' | 'own_only'
    value     = bool(data['value'])

    if field not in ('can_read', 'can_write', 'own_only'):
        return jsonify({'error': 'Invalid field'}), 400

    perm = RolePermissions.query.filter_by(
        role_id=role_id, entity_id=entity_id
    ).first()

    if perm is None:
        perm = RolePermissions(role_id=role_id, entity_id=entity_id)
        db.session.add(perm)

    setattr(perm, field, value)
    db.session.commit()

    return jsonify({'ok': True, 'role_id': role_id,
                    'entity_id': entity_id, 'field': field, 'value': value})
