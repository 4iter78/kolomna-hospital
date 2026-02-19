# ================================================================
# permissions.py — права из БД с кешированием на запрос
#
# Кеш живёт один HTTP-запрос (flask.g).
# При следующем запросе читается из БД заново.
# Это значит: изменил права в БД → следующий запрос уже с новыми.
# ================================================================

from flask import g


def _load_perm(entity_code: str, role_id: int):
    """
    Загружает запись role_permissions из БД (или берёт из кеша g).
    Кеш живёт один HTTP-запрос — не нужен Redis/Memcached.
    """
    if role_id is None:
        return None

    # Инициализируем кеш для текущего запроса
    if not hasattr(g, '_perm_cache'):
        g._perm_cache = {}

    key = (role_id, entity_code)
    if key not in g._perm_cache:
        from models.Entities import Entities
        from models.RolePermissions import RolePermissions

        entity = Entities.query.filter_by(code=entity_code).first()
        if entity:
            perm = RolePermissions.query.filter_by(
                role_id=role_id, entity_id=entity.id
            ).first()
        else:
            perm = None

        g._perm_cache[key] = perm

    return g._perm_cache[key]


def can_read(entity_code: str, role_id: int) -> bool:
    perm = _load_perm(entity_code, role_id)
    return perm.can_read if perm else False


def can_write(entity_code: str, role_id: int) -> bool:
    perm = _load_perm(entity_code, role_id)
    return perm.can_write if perm else False


def is_own_only(entity_code: str, role_id: int) -> bool:
    """
    True — пользователь может работать только со своими записями.
    Используется в контроллерах вместо хардкода списка ролей.
    """
    perm = _load_perm(entity_code, role_id)
    return perm.own_only if perm else False


def get_all_permissions(role_id: int) -> dict:
    """
    Возвращает все права роли в виде словаря:
    { 'work_timetable': {'can_read': True, 'can_write': True, 'own_only': True}, ... }
    Удобно для отладки и страницы администратора.
    """
    from models.RolePermissions import RolePermissions
    from models.Entities import Entities

    perms = (
        RolePermissions.query
        .join(Entities, Entities.id == RolePermissions.entity_id)
        .filter(RolePermissions.role_id == role_id)
        .add_columns(Entities.code)
        .all()
    )
    return {
        code: {
            'can_read':  p.can_read,
            'can_write': p.can_write,
            'own_only':  p.own_only,
        }
        for p, code in perms
    }
