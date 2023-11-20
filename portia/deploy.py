import typing
import uuid

import bcrypt
import click
import nodeenv
import shutil
import os
from pathlib import Path
from subprocess import run, PIPE

import yaml
from flask.cli import FlaskGroup
from portia.factory import create_app as portia_app
from portia.models import User, Goods


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
    users_data = [
        {"username": 'admin@portia.shop', "password": "admin", "is_admin": "Y",
         "name": "관리자", "email": "admin@portia.shop"},
        {"username": 'user@portia.shop', "password": "user", "is_admin": "N",
         "name": "사용자", "email": "user@portia.shop"},
        {"username": 'gdhong@portia.shop', "password": "gdhong", "is_admin": "N",
         "name": "홍길동", "email": "gdhong@portia.shop"}
    ]

    app = create_app()
    with app.app_context():
        for data in users_data:
            enc_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            data["password"] = enc_password.decode('utf-8')
            data["join_date"] = db.func.now()
            db.session.add(User(**data))
        db.session.commit()


def get_yaml(filename):
    product_path = Path(filename)
    if not product_path.exists():
        click.echo("파일이 존재하지 않습니다")
        return False, {}

    with product_path.open() as yaml_file:
        data = yaml.load(yaml_file, yaml.Loader)

    return True, data


@cli.command()
def goods_dummy():
    from portia.models import db

    app = create_app()
    with app.app_context():
        original_file = Path("sample/savethechildren_202311.jpg")

        for i in range(10):
            save_filename = Path(app.config['UPLOAD_FOLDER'], f'{uuid.uuid4()}.jpg')
            shutil.copyfile(original_file, save_filename)

            product_record = Goods()
            product_record.goods_code = f'TS{i}'
            product_record.goods_name = '상품 2'
            product_record.goods_photo = str(save_filename.name)
            product_record.price = 30000
            product_record.goods_cnt = 30
            product_record.goods_description = '상품 2번 등록 테스트'
            product_record.created_date = db.func.now()
            db.session.add(product_record)

            db.session.commit()


if __name__ == "__main__":
    cli()
