from flask import Flask, g, render_template, redirect
from flask_jwt_extended import JWTManager, current_user, get_jwt, jwt_required
from portia.models import db
import json

from portia.utils.route_util import common_context
from portia.utils.social_routes import social_auth
from social_flask.utils import load_strategy
from social_flask_sqlalchemy.models import init_social


def create_app(config_filename):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_file(config_filename, load=json.load)

    jwt = JWTManager(app)
    db.init_app(app)

    app.register_blueprint(social_auth)
    try:
        init_social(app, db.session)
    except:
        pass

    @app.context_processor
    def load_common_context():
        return common_context(
            app.config['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
            load_strategy(),
            getattr(g, 'user', None)
        )
    
    @app.context_processor
    def inject_user():
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}
        
    @app.before_request
    def global_user():
        try:
            g.user = current_user._get_current_object()
        except RuntimeError:
            g.user = None

    @app.route("/")
    def main_page():
        return render_template("index.html")


    @app.route("/short")
    def short():
        return "short!"
    
    @app.route('/logout/')
    @jwt_required()
    def logout():
        """Logout view"""
        jti = get_jwt()["jti"]
        return redirect('/')

    return app
