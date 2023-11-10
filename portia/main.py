import os
import uuid
from pathlib import Path

import bcrypt
from flask import redirect, request, jsonify, render_template
from flask_jwt_extended import (jwt_required, get_jwt, create_access_token,
                                get_jwt_identity, create_refresh_token)
from sqlalchemy import func, or_
from sqlalchemy.exc import NoResultFound

from portia.factory import create_app
from portia.models import db, User, DeliveryAddresses, Goods, Basket
from portia.utils.jwt_utils import admin_required
from portia.utils.validator_utils import Validator
from portia.validate_schema import user_join_schema, login_schema, goods_schema, cart_add_schema, cart_modify_schema

app = create_app(os.getenv("PORTIA_CONFIG", "../config.json"))


@app.route("/api/users/join", methods=["POST"])
def user_join():
    v = Validator(user_join_schema)

    req_json = request.get_json()

    if not v.validate(req_json):
        return jsonify(success=False), 400

    new_user_password = req_json.get('user_password').strip().encode('utf-8')
    encrypt_password = bcrypt.hashpw(new_user_password, bcrypt.gensalt())

    new_username = req_json.get('real_email').strip()

    # 기존 사용자 검색 로직 추가
    exists_user = db.session.execute(db.select(User).
                                     filter(User.username == new_username)).first()
    if exists_user:
        return jsonify(success=False), 400

    # 데이터베이스에 사용자 추가
    new_user = User()
    new_user.username = new_username
    new_user.email = req_json.get('real_email').strip()
    new_user.name = req_json.get('real_name').strip()
    new_user.password = encrypt_password.decode('utf-8')
    new_user.is_admin = 'N'
    new_user.join_date = func.now()

    new_addr = DeliveryAddresses()
    new_addr.username = new_username
    new_addr.user = new_user
    new_addr.postcode = req_json.get('post_code').strip()
    new_addr.address1 = req_json.get('addresses').strip()
    new_addr.address2 = req_json.get('detail_address').strip()
    new_addr.created_date = func.now()

    db.session.add(new_user)
    db.session.add(new_addr)

    db.session.commit()

    return jsonify(success=True)


@app.route("/api/login", methods=["PATCH"])
def login():
    v = Validator(login_schema)

    req_json = request.get_json()

    if not v.validate(req_json):
        return jsonify(success=False), 400

    username = req_json.get("username")
    password = req_json.get("password", '')

    user = db.session.execute(
        db.select(User).filter(User.username == username)).first()
    password_encoded = password.encode('utf-8')

    if not (user and (bcrypt.checkpw(password_encoded, user[0].password.encode('utf-8')))):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, additional_claims={'is_admin': user[0].is_admin == "Y"})
    refresh_token = create_refresh_token(identity=username)

    return jsonify(access_token=access_token, refresh_token=refresh_token, username=username)


@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/api/logout')
@jwt_required()
def logout():
    """Logout view"""
    jti = get_jwt()["jti"]
    return redirect('/')


# placeholder route
# write date: 2023-08-28 19:56
@app.route('/api/placeholder', defaults={'size': '300x200'})
@app.route('/api/placeholder/<size>')
def placeholder_img(size):
    if ('x' not in size) or (size.count('x') != 1):
        return "Bad Request", 400
    width, height = size.split("x")
    bg_fill = '#cccccc'
    txt_fill = '#9c9c9c'
    txt = size

    return (render_template('placeholder.jinja2', width=width, height=height,
                            bg_fill=bg_fill, txt_fill=txt_fill, txt=txt),
            (('Content-Type', 'image/svg+xml'),))


@app.route('/admin/goods/register', methods=["POST"])
@admin_required()
def admin_goods_register():
    v = Validator(goods_schema)

    if not v.validate(request.get_json()):
        return jsonify(success=False), 400

    req_json = request.get_json()

    goods = Goods()
    goods.goods_code = f'GD{uuid.uuid4()}'
    goods.goods_name = req_json.get('goods_name')
    goods.price = req_json.get('price', 0)
    goods.goods_cnt = req_json.get('goods_cnt', 0)
    goods.goods_description = req_json.get('goods_description')
    goods.created_date = db.func.now()

    db.session.add(goods)
    db.session.commit()

    return jsonify(success=True, goods_code=goods.goods_code)


@app.route('/admin/goods/<goods_code>/upload', methods=["POST"])
@admin_required()
def admin_goods_img_upload(goods_code):
    if 'goods_photo' not in request.files:
        return "Bad Request", 400

    upload_file = request.files['goods_photo']
    upload_filename, upload_file_ext = os.path.splitext(upload_file.filename)

    if upload_file_ext not in (".jpeg", ".jpg", ".png", ".gif"):
        return "Bad Request", 400

    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    try:
        save_filename = Path(app.config['UPLOAD_FOLDER'], f'{uuid.uuid4()}{upload_file_ext}')
        upload_file.save(save_filename)

        goods_record = db.session.execute(db.select(Goods).filter(Goods.goods_code == goods_code)).first()[0]
        goods_record.goods_photo = save_filename.name

        # 데이터베이스에서 저장된 파일 이름 반영
        db.session.add(goods_record)
        db.session.commit()

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 400


@app.route('/admin/goods/<goods_code>/modify', methods=["PUT"])
@admin_required()
def admin_goods_modify(goods_code):
    v = Validator(goods_schema)

    if not v.validate(request.get_json()):
        return jsonify(success=False), 400

    req_json = request.get_json()

    goods = db.session.execute(db.select(Goods).filter(Goods.goods_code == goods_code)).first()
    if not goods:
        return "Not Found", 404
    goods = goods[0]
    goods.goods_name = req_json.get('goods_name')
    goods.price = req_json.get('price', 0)
    goods.goods_cnt = req_json.get('goods_cnt', 0)
    goods.goods_description = req_json.get('goods_description')

    db.session.add(goods)
    db.session.commit()

    return jsonify(success=True, goods_code=goods_code)


@app.route('/admin/goods/<goods_code>/delete', methods=["DELETE"])
@admin_required()
def admin_goods_delete(goods_code):
    goods = db.session.execute(db.select(Goods).filter(Goods.goods_code == goods_code)).first()
    if not goods:
        return "Not Found", 404
    db.session.delete(goods[0])
    db.session.commit()

    return jsonify(success=True, goods_code=goods_code)


@app.route('/admin/goods', methods=["GET"])
@admin_required()
def admin_goods_list():
    query_str = request.args.get('query')

    query = db.select(Goods)
    if query_str:
        query = query.filter(or_(Goods.goods_name.ilike(f'%{query_str}%'),
                                 Goods.goods_description.ilike(f'%{query_str}%')))
    query = query.order_by(db.desc(Goods.created_date))

    try:
        page = db.paginate(query, per_page=10)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 400

    resp = {'items': []}
    for item in ('first', 'has_next', 'has_prev', 'last', 'next_num', 'page',
                 'pages', 'per_page', 'prev_num', 'total'):
        resp[item] = getattr(page, item)

    # Page Results
    for row in page.items:
        resp['items'].append({
            'id': row.id,
            'goods_code': row.goods_code,
            'goods_name': row.goods_name,
            'price': row.price,
            'goods_photo': row.goods_photo,
            'goods_cnt': row.goods_cnt,
            'goods_description': row.goods_description,
            'created_date': row.created_date.strftime("%Y%m%d %H:%M")
        })

    return jsonify(success=True, data=resp)


@app.route('/admin/goods/<goods_code>', methods=["GET"])
@admin_required()
def admin_goods_view(goods_code):
    query_res = db.session.execute(
        db.select(Goods).filter(Goods.goods_code == goods_code)).first()
    if not query_res:
        return "NOT FOUND", 404
    row = query_res[0]

    return jsonify({
        'id': row.id,
        'goods_code': row.goods_code,
        'goods_name': row.goods_name,
        'price': row.price,
        'goods_photo': row.goods_photo,
        'goods_cnt': row.goods_cnt,
        'goods_description': row.goods_description,
        'created_date': row.created_date.strftime("%Y%m%d %H:%M")
    })


@app.route("/carts")
@jwt_required()
def carts():
    current_user = get_jwt_identity()

    records = db.session.execute(
        db.select(Basket, Goods).join(Goods).filter(Basket.username == current_user)
    )

    items = [{
        'goods_code': item[1].goods_code,
        'goods_name': item[1].goods_name,
        'price': item[1].price,
        'goods_photo': item[1].goods_photo,
        'goods_description': item[1].goods_description,
        'cart_cnt': item[0].goods_cnt
    } for item in records]

    return jsonify(success=True, data=items)


@app.route("/carts", methods=["POST"])
@jwt_required()
def carts_add():
    req_json = request.get_json()

    v = Validator(cart_add_schema)

    if not v.validate(req_json):
        return jsonify(success=False), 400

    try:
        db.session.execute(
            db.select(Goods).filter(Goods.goods_code == req_json.get('goods_code'))
        ).scalar_one()
    except NoResultFound:
        return jsonify(success=False), 400

    basket = Basket()
    basket.goods = req_json.get('goods_code')
    basket.goods_cnt = req_json.get('goods_cnt')
    basket.username = get_jwt_identity()

    db.session.add(basket)
    db.session.commit()

    return jsonify(success=True)


@app.route("/carts/<goods_code>", methods=["PUT"])
@jwt_required()
def carts_modify(goods_code):
    req_json = request.get_json()

    v = Validator(cart_modify_schema)

    if not v.validate(req_json):
        return jsonify(success=False), 400

    cart_goods = db.session.execute(
        db.select(Basket).filter(Basket.goods == goods_code,
                                 Basket.username == get_jwt_identity())
    ).scalar_one_or_none()

    if not cart_goods:
        return jsonify(success=False), 404

    cart_goods.goods_cnt = req_json.get('goods_cnt')
    db.session.add(cart_goods)
    db.session.commit()

    return jsonify(success=True)


@app.route("/carts/<goods_code>", methods=["DELETE"])
@jwt_required()
def carts_delete(goods_code):
    cart_goods = db.session.execute(
        db.select(Basket).filter(Basket.goods == goods_code,
                                 Basket.username == get_jwt_identity())
    ).scalar_one_or_none()

    if not cart_goods:
        return jsonify(success=False), 404

    db.session.delete(cart_goods)
    db.session.commit()

    return jsonify(success=True)


@app.route("/myinfo")
@jwt_required()
def myinfo_get():
    return jsonify(success=False), 500


@app.route("/myinfo", methods=["PUT"])
@jwt_required()
def myinfo_modify():
    return jsonify(success=False), 500
