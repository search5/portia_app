from flask import Flask
from flask_jwt_extended import JWTManager
from portia.models import db
import json

from portia.routes import shop_admin, shop


def create_app(config_filename):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_file(config_filename, load=json.load)

    jwt = JWTManager(app)
    db.init_app(app)

    app.register_blueprint(shop.bp)
    app.register_blueprint(shop_admin.bp)

    return app
