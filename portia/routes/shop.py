import mimetypes
import os
import uuid

import bcrypt
from flask import redirect, request, jsonify, send_file, \
    url_for, Blueprint, current_app
from flask_jwt_extended import (jwt_required, get_jwt, create_access_token,
                                get_jwt_identity, create_refresh_token)
from sqlalchemy import func, or_
from sqlalchemy.exc import NoResultFound

from portia.models import db, User, DeliveryAddresses, Goods, Basket, Orders, \
    OrdersItem
from portia.utils.placeholder import placeholder_img
from cerberus import Validator
from portia.validate_schema import user_join_schema, login_schema, \
    cart_add_schema, cart_modify_schema, \
    user_modify_schema, order_schema

mimetypes.init()

bp = Blueprint("shop", __name__, url_prefix="/api")


@bp.route("/users/join", methods=["POST"])
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
                                     where(User.username == new_username)).scalar_one_or_none()
    if exists_user:
        return jsonify(success=False), 400

    # 데이터베이스에 사용자 추가
    new_user = User()
    new_user.username = new_username
    new_user.email = req_json.get('real_email').strip()
    new_user.name = req_json.get('real_name').strip()
    new_user.phone = req_json.get('phone').strip()
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


@bp.route("/login", methods=["PATCH"])
def login():
    v = Validator(login_schema)

    req_json = request.get_json()

    if not v.validate(req_json):
        return jsonify(success=False), 400

    username = req_json.get("username")
    password = req_json.get("password", '')

    user = db.session.execute(
        db.select(User).where(User.username == username)).scalar_one_or_none()
    password_encoded = password.encode('utf-8')

    if not (user and (bcrypt.checkpw(password_encoded, user.password.encode('utf-8')))):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, additional_claims={'is_admin': user.is_admin == "Y"})
    refresh_token = create_refresh_token(identity=username)

    return jsonify(access_token=access_token, refresh_token=refresh_token, username=username)


@bp.route('/logout')
@jwt_required()
def logout():
    """Logout view"""
    jti = get_jwt()["jti"]
    return redirect('/')


@bp.route("/carts")
@jwt_required()
def carts():
    current_user = get_jwt_identity()

    records = db.session.execute(
        db.select(Basket, Goods).join(Goods).where(Basket.username == current_user)
    )

    items = [{
        'id': item[0].id,
        'goods_code': item[1].goods_code,
        'goods_name': item[1].goods_name,
        'price': item[1].price,
        'goods_photo_url': url_for('goods_img_view', goods_code=item[1].goods_code, img_path=item[1].goods_photo or ''),
        'goods_description': item[1].goods_description,
        'cart_cnt': item[0].goods_cnt
    } for item in records]

    return jsonify(success=True, data=items)


@bp.route("/carts", methods=["POST"])
@jwt_required()
def carts_add():
    req_json = request.get_json()

    v = Validator(cart_add_schema)

    if not v.validate(req_json):
        return jsonify(success=False), 400

    try:
        db.session.execute(
            db.select(Goods).where(Goods.goods_code == req_json.get('goods_code'))
        ).scalar_one()
    except NoResultFound:
        return jsonify(success=False), 400

    basket = Basket()
    basket.goods_code = req_json.get('goods_code')
    basket.goods_cnt = req_json.get('goods_cnt')
    basket.username = get_jwt_identity()

    db.session.add(basket)
    db.session.commit()

    return jsonify(success=True)


@bp.route("/carts/<goods_code>", methods=["PUT"])
@jwt_required()
def carts_modify(goods_code):
    req_json = request.get_json()

    v = Validator(cart_modify_schema)

    if not v.validate(req_json):
        return jsonify(success=False), 400

    cart_goods = db.session.execute(
        db.select(Basket).where(Basket.goods_code == goods_code,
                                Basket.username == get_jwt_identity())
    ).scalar_one_or_none()

    if not cart_goods:
        return jsonify(success=False), 404

    cart_goods.goods_cnt = req_json.get('goods_cnt')
    db.session.add(cart_goods)
    db.session.commit()

    return jsonify(success=True)


@bp.route("/carts/<goods_code>", methods=["DELETE"])
@jwt_required()
def carts_delete(goods_code):
    cart_goods = db.session.execute(
        db.select(Basket).where(Basket.goods_code == goods_code,
                                Basket.username == get_jwt_identity())
    ).scalar_one_or_none()

    if not cart_goods:
        return jsonify(success=False), 404

    db.session.delete(cart_goods)
    db.session.commit()

    return jsonify(success=True)


@bp.route("/carts", methods=["DELETE"])
@jwt_required()
def carts_delete_all():
    db.session.execute(db.delete(Basket).where(Basket.username == get_jwt_identity()))
    db.session.commit()

    return jsonify(success=True)


@bp.route("/myinfo")
@jwt_required()
def myinfo_get():
    current_user = get_jwt_identity()

    record = db.session.execute(db.select(User).where(User.username == current_user)).scalar_one()
    user_delivery_addresses = record.addresses[0].todict() if record.addresses else dict()

    user_data = dict(
        real_name=record.name,
        real_email=record.email,
        real_phone=record.phone,
        post_code=user_delivery_addresses.get('postcode', ''),
        addresses=user_delivery_addresses.get('address1', ''),
        detail_address=user_delivery_addresses.get('address2', '')
    )

    return jsonify(success=True, **user_data)


@bp.route("/myinfo", methods=["PUT"])
@jwt_required()
def myinfo_modify():
    current_user = get_jwt_identity()

    req_json = request.get_json()
    current_password = req_json.get('user_current_password').encode('utf-8')

    validate_schema = user_modify_schema
    if not current_password:
        del validate_schema['user_current_password']
        del validate_schema['user_new_password']
        del validate_schema['user_new_password_confirm']

    v = Validator(validate_schema)

    if not v.validate(req_json):
        return jsonify(success=False), 400

    user_record = db.session.execute(db.select(User).where(User.username == current_user)).scalar_one()
    user_delivery_addresses = db.session.execute(
        db.select(DeliveryAddresses).where(DeliveryAddresses.username == current_user)).scalar_one_or_none()
    if not user_delivery_addresses:
        user_delivery_addresses = DeliveryAddresses()
        user_delivery_addresses.username = current_user
        user_delivery_addresses.created_date = db.func.now()

    user_record.name = req_json.get('real_name')
    user_record.email = req_json.get('real_email')
    user_record.phone = req_json.get('real_phone')

    # check pw
    if current_password:
        new_password = req_json.get('user_new_password').encode('utf-8')
        new_password_confirm = req_json.get('user_new_password_confirm').encode('utf-8')

        new_password_equal = new_password == new_password_confirm

        # 사용자가 입력한 비밀번호가 저장되어 있는 비밀번호와 일치하는지 확인될 때만 비밀번호 변경을 수행한다.
        if bcrypt.checkpw(current_password, user_record.password.encode('utf-8')) and new_password_equal:
            encrypt_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
            user_record.password = encrypt_password.decode('utf-8')

    user_delivery_addresses.postcode = req_json.get('post_code')
    user_delivery_addresses.address1 = req_json.get('addresses')
    user_delivery_addresses.address2 = req_json.get('detail_address')

    db.session.add(user_record)
    db.session.add(user_delivery_addresses)

    db.session.commit()

    return jsonify(success=True)


@bp.route("/myinfo/orders")
@jwt_required()
def myinfo_orders():
    current_user = get_jwt_identity()

    order_records = db.select(Orders).where(Orders.username == current_user).order_by(db.desc(Orders.order_date))

    try:
        page = db.paginate(order_records, per_page=10)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 400

    resp = {'items': []}
    for item in ('first', 'has_next', 'has_prev', 'last', 'next_num', 'page',
                 'pages', 'per_page', 'prev_num', 'total'):
        resp[item] = getattr(page, item)

    # Page Results
    for row in page.items:
        resp['items'].append({
            "uuid": row.order_str_id,
            "title": row.order_summary_title,
            "img": url_for('goods_img_view', **row.order_representative_image_info),
            "price": row.order_total_price,
            "order_date": row.order_date.strftime('%Y-%m-%d')
        })

    return jsonify(success=True, data=resp)


@bp.route("/myinfo/orders/latest")
@jwt_required()
def myinfo_orders_latest():
    current_user = get_jwt_identity()

    order_records = db.session.execute(
        db.select(Orders).where(Orders.username == current_user).order_by(db.desc(Orders.order_date)).limit(5)
    ).scalars()

    items = []
    for item in order_records:
        items.append({
            "uuid": item.order_str_id,
            "title": item.order_summary_title,
            "img": url_for('goods_img_view', **item.order_representative_image_info),
            "price": item.order_total_price,
            "order_date": item.order_date.strftime('%Y-%m-%d')
        })

    return jsonify(success=True, items=items)


@bp.route("/myinfo/orders/<order_id>")
@jwt_required()
def myinfo_orders_detail(order_id):
    order_record:  Orders = db.session.execute(
        db.select(Orders).where(Orders.order_str_id == order_id)
    ).scalar_one_or_none()

    if not order_record:
        return jsonify(success=False), 404

    data = {
        "order_no": order_record.order_str_id,
        "order_date": order_record.order_date.strftime('%Y-%m-%d'),
        "items": [
            {
                "goods_name": '상품 1',
                "goods_cnt": 2,
                "goods_price": 30000,
                "goods_total_price": 60000,
            }
        ],
        "orderers": {
            "name": order_record.user.name,
            "phone": order_record.user.phone
        },
        "ship_to": {
            "name": order_record.ship_to_name,
            "phone": order_record.ship_to_phone,
            "addresses": order_record.ship_to_addresses,
            "post_code": order_record.ship_to_postcode
        },
        "order_status": order_record.order_status
    }

    return jsonify(success=True, data=data), 200


@bp.route("/goods/<goods_code>/img/<img_path>")
def goods_img_view(goods_code, img_path):
    mime, _ = mimetypes.guess_type(img_path)

    serving_img_path = os.path.join(current_app.config.get("UPLOAD_FOLDER"), img_path)
    if os.path.exists(serving_img_path):
        return send_file(serving_img_path, mimetype=mime)
    else:
        return placeholder_img('500x500')


@bp.route("/goods")
def goods_list():
    query_str = request.args.get('keyword')
    limit = request.args.get('limit', 9, type=int)

    query = db.select(Goods)
    if query_str:
        query = query.where(or_(Goods.goods_name.ilike(f'%{query_str}%'),
                                Goods.goods_description.ilike(f'%{query_str}%')))
    query = query.order_by(db.desc(Goods.created_date))

    try:
        page = db.paginate(query, per_page=limit)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 400

    resp = {'items': []}
    for item in ('first', 'has_next', 'has_prev', 'last', 'next_num', 'page',
                 'pages', 'per_page', 'prev_num', 'total'):
        resp[item] = getattr(page, item)

    # Page Results
    for row in page.items:
        resp['items'].append({
            'goods_code': row.goods_code,
            'goods_name': row.goods_name,
            'price': row.price,
            'goods_photo_url': url_for('goods_img_view', goods_code=row.goods_code, img_path=row.goods_photo or ''),
            'goods_cnt': row.goods_cnt,
            'goods_description': row.goods_description,
            'created_date': row.created_date.strftime("%Y%m%d %H:%M")
        })

    return jsonify(success=True, data=resp)


@bp.route("/goods/<goods_code>")
def goods_detail(goods_code):
    row = db.session.execute(
        db.select(Goods).where(Goods.goods_code == goods_code)).scalar_one_or_none()
    if not row:
        return jsonify(success=False), 404

    return jsonify({
        'goods_code': row.goods_code,
        'goods_name': row.goods_name,
        'price': row.price,
        'goods_photo_url': url_for('goods_img_view', goods_code=row.goods_code, img_path=row.goods_photo or ''),
        'goods_cnt': row.goods_cnt,
        'goods_description': row.goods_description,
        'created_date': row.created_date.strftime("%Y%m%d %H:%M")
    })


@bp.route("/orders", methods=["POST"])
@jwt_required()
def order():
    current_user = get_jwt_identity()

    req_json = request.get_json()

    v = Validator(order_schema)

    if not v.validate(req_json):
        return jsonify(success=False), 400

    ship_to_info = req_json.get('ship_to')

    # 주문 정보 입력
    order_record = Orders()
    order_record.order_str_id = f'GD{uuid.uuid4()}'
    order_record.username = current_user
    order_record.order_date = db.func.now()
    order_record.ship_to_name = ship_to_info.get('name')
    order_record.ship_to_phone = ship_to_info.get('phone')
    order_record.ship_to_addresses = ship_to_info.get('addresses')
    order_record.ship_to_postcode = ship_to_info.get('post_code')
    order_record.order_status = '결제중'
    db.session.add(order_record)

    # 주문 상세 정보 입력(주문 제품)
    for goods in req_json.get('items', []):
        record = OrdersItem()
        record.order_str_id = order_record.order_str_id
        record.goods_code = goods.get('goods_code')
        record.goods_price = goods.get('goods_price')
        record.goods_cnt = goods.get('goods_cnt')
        db.session.add(record)

    db.session.commit()

    return jsonify(success=True)
