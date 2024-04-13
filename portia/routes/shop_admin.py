import mimetypes
import os
import uuid
from pathlib import Path

from flask import request, jsonify, send_file, url_for, Blueprint, current_app

from sqlalchemy import or_

from portia.models import db, Goods
from portia.utils.jwt_utils import admin_required
from cerberus import Validator
from portia.validate_schema import goods_schema

mimetypes.init()

bp = Blueprint("shop_admin", __name__, url_prefix="/api/admin")


@bp.route('/goods/register', methods=["POST"])
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


@bp.route('/goods/<goods_code>/upload', methods=["POST"])
@admin_required()
def admin_goods_img_upload(goods_code):
    if 'goods_photo' not in request.files:
        return "Bad Request", 400

    upload_file = request.files['goods_photo']
    upload_filename, upload_file_ext = os.path.splitext(upload_file.filename)

    if upload_file_ext not in (".jpeg", ".jpg", ".png", ".gif"):
        return "Bad Request", 400

    Path(current_app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    try:
        save_filename = Path(current_app.config['UPLOAD_FOLDER'], f'{uuid.uuid4()}{upload_file_ext}')
        upload_file.save(save_filename)

        goods_record = db.session.execute(db.select(Goods).where(Goods.goods_code == goods_code)).scalar_one()
        goods_record.goods_photo = save_filename.name

        # 데이터베이스에서 저장된 파일 이름 반영
        db.session.add(goods_record)
        db.session.commit()

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 400


@bp.route('/goods/<goods_code>/modify', methods=["PUT"])
@admin_required()
def admin_goods_modify(goods_code):
    v = Validator(goods_schema)

    if not v.validate(request.get_json()):
        return jsonify(success=False), 400

    req_json = request.get_json()

    goods = db.session.execute(db.select(Goods).where(Goods.goods_code == goods_code)).scalar_one_or_none()
    if not goods:
        return jsonify(success=False), 404
    goods.goods_name = req_json.get('goods_name')
    goods.price = req_json.get('price', 0)
    goods.goods_cnt = req_json.get('goods_cnt', 0)
    goods.goods_description = req_json.get('goods_description')

    db.session.add(goods)
    db.session.commit()

    return jsonify(success=True, goods_code=goods_code)


@bp.route('/goods/<goods_code>/delete', methods=["DELETE"])
@admin_required()
def admin_goods_delete(goods_code):
    goods = db.session.execute(db.select(Goods).where(Goods.goods_code == goods_code)).scalar_one_or_none()
    if not goods:
        return jsonify(success=False), 404
    db.session.delete(goods)
    db.session.commit()

    return jsonify(success=True, goods_code=goods_code)


@bp.route('/goods', methods=["GET"])
@admin_required()
def admin_goods_list():
    query_str = request.args.get('query')

    query = db.select(Goods)
    if query_str:
        query = query.where(or_(Goods.goods_name.ilike(f'%{query_str}%'),
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
            'goods_photo_url': url_for('admin_goods_img_view', goods_code=row.goods_code, img_path=row.goods_photo or ''),
            'goods_photo': row.goods_photo,
            'goods_cnt': row.goods_cnt,
            'goods_description': row.goods_description,
            'created_date': row.created_date.strftime("%Y%m%d %H:%M")
        })

    return jsonify(success=True, data=resp)


@bp.route('/goods/<goods_code>', methods=["GET"])
@admin_required()
def admin_goods_view(goods_code):
    row = db.session.execute(
        db.select(Goods).where(Goods.goods_code == goods_code)).scalar_one_or_none()
    if not row:
        return jsonify(success=False), 404

    return jsonify({
        'id': row.id,
        'goods_code': row.goods_code,
        'goods_name': row.goods_name,
        'price': row.price,
        'goods_photo_url': url_for('admin_goods_img_view', goods_code=row.goods_code, img_path=row.goods_photo or ''),
        'goods_cnt': row.goods_cnt,
        'goods_description': row.goods_description,
        'created_date': row.created_date.strftime("%Y%m%d %H:%M")
    })


@bp.route("/goods/<goods_code>/img/<img_path>")
def admin_goods_img_view(goods_code, img_path):
    mime, _ = mimetypes.guess_type(img_path)

    serving_img_path = os.path.join(current_app.config.get("UPLOAD_FOLDER"), img_path)
    if os.path.exists(serving_img_path):
        return send_file(serving_img_path, mimetype=mime)
    else:
        return placeholder_img('500x500')
