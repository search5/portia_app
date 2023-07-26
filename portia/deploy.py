import bcrypt
import click
import nodeenv
import shutil
import os
from pathlib import Path
from subprocess import run, PIPE
from flask.cli import FlaskGroup
from portia.factory import create_app as portia_app
from portia.models import User


def create_app():
    return portia_app(os.getenv("PORTIA_CONFIG", "../config.json"))


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""


@cli.command()
def nodejs_setup():
    """Node.JS Installation"""

    print("Node.JS Install")
    print("-" * 80)
    parser = nodeenv.make_parser()
    parse_result = parser.parse_args(["-n", "lts", "-p"])

    src_domain = 'nodejs.org'
    nodeenv.src_base_url = 'https://%s/download/release' % src_domain

    parse_result.node = nodeenv.get_last_lts_node_version()

    env_dir = nodeenv.get_env_dir(parse_result)
    nodeenv.create_environment(env_dir, parse_result)
    print("-" * 80)

    os.chdir("portia_web")
    run(["npm", "install"], stdout=PIPE, stderr=PIPE)

    return True


@cli.command()
def frontend_ready():
    """Vite.js Build File to portia_app"""

    portia_dir = Path("portia")
    portia_assets_dir = portia_dir / "static"
    portia_templates_dir = portia_dir / "templates"

    portia_templates_dir.mkdir(exist_ok=True)
    if portia_assets_dir.exists():
        shutil.rmtree(portia_assets_dir)
    
    shutil.copy("portia_web/dist/index.html", portia_templates_dir / "index.html")
    shutil.copytree("portia_web/dist/assets", "portia/static")


@cli.command()
def init_db():
    """Database Initialize"""

    # from social_flask_sqlalchemy import models
    from portia.models import db

    app = create_app()
    with app.app_context():
        db.create_all()


@cli.command()
def init_user():
    """Initialize User"""
    from portia.models import db
    encrypt_password = bcrypt.hashpw('jiho'.encode('utf-8'), bcrypt.gensalt())

    app = create_app()
    with app.app_context():
        user = User(username='jiho', password=encrypt_password.decode('utf-8'), is_admin='Y',
                    join_date=db.func.now(), name='이지호',
                    email='search5@gmail.com')
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    cli()
