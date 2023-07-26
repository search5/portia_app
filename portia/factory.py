from flask import Flask, g, render_template, redirect
from flask_jwt_extended import JWTManager, current_user, get_jwt, jwt_required
from portia.models import db
import json


def create_app(config_filename):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_file(config_filename, load=json.load)

    jwt = JWTManager(app)
    db.init_app(app)

    # @jwt.encode_key_loader
    # def encode_key_loader(value):
    #     print('=' * 80)
    #     print(value)
    #     print('=' * 80)
    #     return 'abc'
    #
    # @jwt.decode_key_loader
    # def decode_key_loader(header, payload):
    #     print('-' * 80)
    #     print(header)
    #     print(payload)
    #     print('-' * 80)
    #     return 'abc'

    return app
