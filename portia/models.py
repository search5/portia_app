from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()


class JSONMixin:
    def todict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class User(db.Model, JSONMixin):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(40), nullable=False)