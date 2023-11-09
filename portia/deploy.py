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
    encrypt_password = bcrypt.hashpw('jiho'.encode('utf-8'), bcrypt.gensalt())

    app = create_app()
    with app.app_context():
        user = User(username='jiho', password=encrypt_password.decode('utf-8'), is_admin='Y',
                    join_date=db.func.now(), name='이지호',
                    email='search5@gmail.com')
        db.session.add(user)
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
        for i in range(10):
            product_record = Goods()
            product_record.goods_code = f'TS{i}'
            product_record.goods_name = '상품 2'
            product_record.price = 30000
            product_record.goods_cnt = 30
            product_record.goods_description = '상품 2번 등록 테스트'
            product_record.created_date = db.func.now()
            db.session.add(product_record)

            db.session.commit()


@cli.command()
@click.argument('filename')
def product_register(filename):
    from portia.models import db

    app = create_app()
    with app.app_context():
        success, data = get_yaml(filename)

        if not success:
            return

        # 이미 등록되어 있는 상품인지 확인
        product_record = db.session.execute(db.select(Goods).filter(Goods.goods_code == data['goods_code'])).first()
        if product_record:
            click.echo('등록된 제품은 다시 등록할 수 없습니다')
            return

        product_record = Goods()

        for key, val in data.items():
            setattr(product_record, key, val)

        db.session.add(product_record)

        db.session.commit()

        click.echo(product_record.id)


@cli.command()
@click.argument('filename')
def product_edit(filename):
    from portia.models import db

    app = create_app()
    with app.app_context():
        success, data = get_yaml(filename)

        if not success:
            return
        # 제품 정보 업데이트 시 상품 수량은 업데이트하지 않도록 한다.
        if 'goods_cnt' in data:
            del data['goods_cnt']

        # 이미 등록되어 있는 상품인지 확인
        product_record = db.session.execute(db.select(Goods).filter(Goods.goods_code == data['goods_code'])).first()
        if not product_record:
            click.echo('등록되지 않은 제품은 수정할 수 없습니다')
            return

        for key, val in data.items():
            setattr(product_record, key, val)

        # db.session.add(product_record)

        db.session.commit()

        click.echo(product_record.id)


if __name__ == "__main__":
    cli()
