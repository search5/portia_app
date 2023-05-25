from portia.factory import create_app
import os
from social_flask_sqlalchemy.models import init_social
from portia.models import db

app = create_app(os.getenv("PORTIA_CONFIG", "../config.json"))

