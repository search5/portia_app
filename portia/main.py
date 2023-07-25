import os

from flask import render_template, redirect, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, get_jwt_identity, create_refresh_token

from portia.factory import create_app

app = create_app(os.getenv("PORTIA_CONFIG", "../config.json"))


@app.route("/api/login")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token)


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
