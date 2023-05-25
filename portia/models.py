from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_login import UserMixin

db = SQLAlchemy()


class JSONMixin:
    def todict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class User(db.Model, UserMixin, JSONMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
