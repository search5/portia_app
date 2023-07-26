from flask import Flask, g, render_template, redirect
from flask_jwt_extended import JWTManager, current_user, get_jwt, jwt_required
from portia.models import db
import json


def create_app(config_filename):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_file(config_filename, load=json.load)

    jwt = JWTManager(app)
    db.init_app(app)

    return app
