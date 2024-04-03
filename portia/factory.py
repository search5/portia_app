from flask import Flask
from flask_jwt_extended import JWTManager
from portia.models import db
import json


def create_app(config_filename):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_file(config_filename, load=json.load)

    jwt = JWTManager(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
