import uuid
import shutil
import os

from pathlib import Path

import bcrypt

from portia.factory import create_app
from portia.models import User, Goods

app = create_app(os.getenv("PORTIA_CONFIG", "../config.json"))


@app.cli.command()
def init_db():
    """Database Initialize"""

    # from social_flask_sqlalchemy import models
    from portia.models import db

    with app.app_context():
        db.create_all()


@app.cli.command()
def init_user():
    """Initialize User"""
    from portia.models import db
    users_data = [
        {"username": 'admin@portia.shop', "password": "admin", "is_admin": "Y",
         "name": "관리자", "email": "admin@portia.shop", "phone": "010-1234-5678"},
        {"username": 'user@portia.shop', "password": "user", "is_admin": "N",
         "name": "사용자", "email": "user@portia.shop", "phone": "010-1234-5678"},
        {"username": 'gdhong@portia.shop', "password": "gdhong", "is_admin": "N",
         "name": "홍길동", "email": "gdhong@portia.shop", "phone": "010-1234-5678"}
    ]

    with app.app_context():
        for data in users_data:
            enc_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            data["password"] = enc_password.decode('utf-8')
            data["join_date"] = db.func.now()
            db.session.add(User(**data))
        db.session.commit()


@app.cli.command()
def goods_dummy():
    from portia.models import db

    with app.app_context():
        original_file = Path("sample/sample.jpg")

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


@app.cli.command()
def orders_dummy():
    order_table_columns = ('order_str_id', 'username', 'order_date', 'ship_to_name',
                           'ship_to_phone', 'ship_to_addresses', 'ship_to_postcode',
                           'order_status')
    order_item_table_columns = ('order_str_id', 'goods_code', 'goods_price', 'goods_cnt')

    from portia.models import db, Orders, OrdersItem

    with app.app_context():
        order_values = (
            ('7777578724', 'user@portia.shop', db.func.now(), '홍길동', '010-1234-5678', '경기도 고양시', '10346', '배송중'),
            ('4235538724', 'user@portia.shop', db.func.now(), '홍길동', '010-1234-5678', '경기도 고양시', '10346', '배송중')
        )

        order_item_values = (
            ('4235538724', 'TS0', 300, 1),
            ('4235538724', 'TS0', 300, 5),
            ('7777578724', 'TS1', 500, 1),
            ('7777578724', 'TS5', 800, 5)
        )

        for item in order_values:
            record = Orders(**dict(zip(order_table_columns, item)))
            db.session.add(record)

        for item in order_item_values:
            record = OrdersItem(**dict(zip(order_item_table_columns, item)))
            db.session.add(record)

        db.session.commit()