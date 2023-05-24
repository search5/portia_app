from flask import Flask, g
from flask_jwt_extended import JWTManager
from portia.models import db
import json


from portia.utils.route_util import common_context

from social_flask.utils import load_strategy


def create_app(config_filename):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_file(config_filename, load=json.load)

    jwt = JWTManager(app)
    db.init_app(app)

    @app.context_processor
    def load_common_context():
        return common_context(
            app.config['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
            load_strategy(),
            getattr(g, 'user', None)
        )

    return app
