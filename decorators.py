from functools import wraps
from flask import session, request, abort, redirect, url_for
from permissions import can_read, can_write, is_own_only


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth_controller.login', next=request.path))
        return f(*args, **kwargs)
    return wrapper


def access_control(entity):
    """
    GET              → can_read(entity, role)
    POST/PUT/DELETE  → can_write(entity, role)
    Всё из БД через permissions.py. roles.py не используется.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role = session.get('user_role')
            if request.method == 'GET':
                if not can_read(entity, role):
                    abort(403)
            else:
                if not can_write(entity, role):
                    abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def access_control_with_ownership(entity, get_entry_owner_id):
    """
    Как access_control, плюс для PUT/DELETE проверяет own_only из БД.
    Если own_only=True — пользователь может менять только свои записи.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role    = session.get('user_role')
            user_id = session.get('user_id')

            if request.method == 'GET':
                if not can_read(entity, role):
                    abort(403)
            else:
                if not can_write(entity, role):
                    abort(403)
                if is_own_only(entity, role):
                    entry_id = next(iter(kwargs.values()), None)
                    if entry_id is not None:
                        owner_id = get_entry_owner_id(entry_id)
                        if owner_id != user_id:
                            abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorator
