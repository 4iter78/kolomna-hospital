from app import db_connection

db = db_connection


class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'

    id        = db.Column(db.Integer, primary_key=True)
    role_id   = db.Column(db.Integer, db.ForeignKey('user_roles.id',
                          ondelete='CASCADE'), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id',
                          ondelete='CASCADE'), nullable=False)
    can_read  = db.Column(db.Boolean, nullable=False, default=False)
    can_write = db.Column(db.Boolean, nullable=False, default=False)
    own_only  = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        db.UniqueConstraint('role_id', 'entity_id', name='uq_role_entity'),
    )

    def __json__(self):
        return {
            'id':        self.id,
            'role_id':   self.role_id,
            'entity_id': self.entity_id,
            'can_read':  self.can_read,
            'can_write': self.can_write,
            'own_only':  self.own_only,
        }

    def __repr__(self):
        return (f'<RolePermissions role={self.role_id} '
                f'entity={self.entity_id} '
                f'r={self.can_read} w={self.can_write} own={self.own_only}>')
