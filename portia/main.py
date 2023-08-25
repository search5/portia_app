import os

import bcrypt
from cerberus import Validator
from flask import redirect, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, get_jwt_identity, create_refresh_token
from sqlalchemy import func

from portia.factory import create_app
from portia.models import db, User, DeliveryAddresses

app = create_app(os.getenv("PORTIA_CONFIG", "../config.json"))


@app.route("/api/users/join", methods=["POST"])
def user_join():
    schema = {'real_name': {'type': 'string', 'minlength': 1},
              'real_email': {'type': 'string', 'minlength': 1},
              'user_password': {'type': 'string', 'minlength': 1},
              'post_code': {'type': 'string', 'minlength': 5, 'maxlength': 5},
              'addresses': {'type': 'string', 'minlength': 5},
              'detail_address': {'type': 'string', 'minlength': 5}}
    v = Validator(schema)

    req_json = request.get_json()

    if not v.validate(req_json):
        return jsonify(success=False), 400

    # 데이터베이스에 사용자 추가
    new_user = User()
    new_user.username = req_json.get('real_email')
    new_user.email = req_json.get('real_email')
    new_user.name = req_json.get('real_name')
    new_user.password = req_json.get('user_password')
    new_user.is_admin = 'N'
    new_user.join_date = func.now()

    user_addr = DeliveryAddresses()
    user_addr.username = req_json.get('real_email')
    user_addr.user = new_user
    user_addr.postcode = req_json.get('post_code')
    user_addr.address1 = req_json.get('addresses')
    user_addr.address2 = req_json.get('detail_address')
    user_addr.created_date = func.now()

    db.session.add(new_user)
    db.session.add(user_addr)

    db.session.commit()

    return jsonify(success=True)


@app.route("/api/login", methods=["PATCH"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = db.session.execute(
        db.select(User).filter(User.username == username)).first()
    password_encoded = password.encode('utf-8')

    if not (user and (bcrypt.checkpw(password_encoded, user[0].password.encode('utf-8')))):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/api/short")
def short():
    return "short!"


@app.route('/api/logout/')
@jwt_required()
def logout():
    """Logout view"""
    jti = get_jwt()["jti"]
    return redirect('/')
