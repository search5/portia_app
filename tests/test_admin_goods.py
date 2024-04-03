import io
from pathlib import Path

import pytest


@pytest.fixture()
def cleanup_goods(client):
    from portia.models import Goods, db
    from portia.main import app

    # success data clean
    with app.app_context():
        r = db.session.execute(db.select(Goods))
        for row in r:
            if row.goods_code.startswith("TS"):
                continue
            if row.goods_photo:
                img = Path(row.goods_photo)
                if img.exists():
                    img.unlink()
            db.session.delete(row)

        db.session.commit()


def test_admin_goods_register_success(client, cleanup_goods, admin_authorization):
    # 상품 등록 기능
    res = client.post("/api/admin/goods/register", json={
        'goods_name': '상품 1',
        'price': 30000,
        'goods_cnt': 1,
        'goods_description': '상품 등록 테스트'
    }, headers=[admin_authorization])
    assert res.status_code == 200, res.status_code


def test_admin_goods_register_notsend_failure(client, admin_authorization):
    # 상품 등록 실패(아무것도 안 보냄)
    res = client.post("/api/admin/goods/register", json={}, headers=[admin_authorization])
    assert res.status_code == 400, res.status_code


def test_admin_goods_register_failure(client, admin_authorization):
    # 상품 등록 실패(의도적으로 잘못된 데이터 보냄)
    res = client.post("/api/admin/goods/register", json={
        'goods_name': '',
        'price': 0,
        'goods_cnt': 0,
        'goods_description': ''
    }, headers=[admin_authorization])
    assert res.status_code == 400, res.status_code


def test_admin_goods_image_upload(client, admin_authorization):
    goods_code = goods_register(client, admin_authorization)

    sample_file_name = "sample/savethechildren_202311.jpg"
    post_data = {'goods_photo': (io.BytesIO(open(sample_file_name, "rb").read()), sample_file_name)}

    res = client.post(f'/api/admin/goods/{goods_code}/upload', data=post_data,
                      headers=[admin_authorization])

    assert res.status_code == 200, res.text


def test_admin_goods_image_upload_failure_not_allowed_file(client, admin_authorization):
    res = client.post(f'/api/admin/goods/abcde/upload', data={'goods_photo': (io.BytesIO(b""), "image.php")},
                      headers=[admin_authorization])
    assert res.status_code == 400


def test_admin_goods_image_upload_failure_not_upload(client, admin_authorization):
    res = client.post(f'/api/admin/goods/abcde/upload', data={},
                      headers=[admin_authorization])
    assert res.status_code == 400


def test_admin_goods_image_upload_failure_bad_code(client, admin_authorization):
    res = client.post(f'/api/admin/goods/abcde/upload', data={'goods_photo': (io.BytesIO(b""), "image.jpg")},
                      headers=[admin_authorization])
    assert res.status_code == 400


def goods_register(client, admin_authorization):
    res = client.post("/api/admin/goods/register", json={
        'goods_name': '상품 2',
        'price': 30000,
        'goods_cnt': 1,
        'goods_description': '상품 2번 등록 테스트'
    }, headers=[admin_authorization])
    assert res.status_code == 200, res.status_code

    return res.get_json().get('goods_code')


def test_admin_goods_modify_success(client, admin_authorization):
    # 상품 수정 기능
    goods_code = goods_register(client, admin_authorization)

    res = client.put(f"/api/admin/goods/{goods_code}/modify", json={
        'goods_name': '상품 2-1',
        'price': 50000,
        'goods_cnt': 2,
        'goods_description': '상품 2번 수정 테스트'
    }, headers=[admin_authorization])
    assert res.status_code == 200, res.status_code


def test_admin_goods_modify_failure_invalid_goods(client, admin_authorization):
    # 상품 수정 기능(잘못된 상품 아이디)
    res = client.put("/api/admin/goods/like/modify", json={
        'goods_name': '상품 2-1',
        'price': 50000,
        'goods_cnt': 2,
        'goods_description': '상품 2번 수정 테스트'
    }, headers=[admin_authorization])
    assert res.status_code == 404, res.status_code


def test_admin_goods_modify_failure_invalid_data(client, admin_authorization):
    # 상품 수정 기능(잘못된 데이터 전송)
    res = client.put("/api/admin/goods/1/modify", json={}, headers=[admin_authorization])
    assert res.status_code == 400, res.status_code


def test_admin_goods_delete_success(client, admin_authorization):
    # 상품 삭제 기능
    goods_code = goods_register(client, admin_authorization)

    res = client.delete(f"/api/admin/goods/{goods_code}/delete",
                        headers=[admin_authorization])
    assert res.status_code == 200, res.status_code


def test_admin_goods_delete_failure(client, admin_authorization):
    # 상품 삭제 기능
    res = client.delete("/api/admin/goods/1/delete", json={}, headers=[admin_authorization])
    assert res.status_code == 404, res.status_code


def test_admin_goods_list_success(client, admin_authorization):
    # 등록된 상품 목록 반환 기능
    res = client.get("/api/admin/goods", headers=[admin_authorization])
    assert res.status_code == 200, res.status_code


def test_admin_goods_list_failure(client, admin_authorization):
    # 등록된 상품 목록 반환 기능
    res = client.get("/api/admin/goods?page=alpha", headers=[admin_authorization])
    assert res.status_code == 400, res.text


def test_admin_goods_list_success_query_str(client, admin_authorization):
    # 등록된 상품 목록 반환 기능
    res = client.get("/api/admin/goods?query=alpha", headers=[admin_authorization])
    assert res.status_code == 200, res.text


def test_admin_goods_get_success(client, admin_authorization):
    # 등록된 상품의 상세 정보 가져오기
    goods_code = goods_register(client, admin_authorization)

    res = client.get(f"/api/admin/goods/{goods_code}", headers=[admin_authorization])
    assert res.status_code == 200, res.status_code


def test_admin_goods_get_failure_bad_code(client, admin_authorization):
    # 등록된 상품의 상세 정보 가져오기
    res = client.get("/api/admin/goods/alpha", headers=[admin_authorization])
    assert res.status_code == 404, res.status_code


def test_admin_goods_image_success(client, admin_authorization):
    res = client.get("/api/admin/goods/TS0/img/3f116911-afed-4455-8987-bb7ab17b21e7.jpg", headers=[admin_authorization])
    assert res.status_code == 200, res.text


def test_admin_goods_image_failure(client, admin_authorization):
    res = client.get("/api/admin/goods/TS0/img/alpha.jpg", headers=[admin_authorization])
    assert res.status_code == 200, res.text