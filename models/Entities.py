from app import db_connection

db = db_connection


class Entities(db.Model):
    __tablename__ = 'entities'

    id   = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    permissions = db.relationship('RolePermissions', backref='entity',
                                  lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Entity {self.code}>'
