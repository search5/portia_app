import pytest


@pytest.fixture()
def cleanup_carts(client):
    from portia.models import Basket, db
    from portia.main import app

    # success data clean
    with app.app_context():
        r = db.session.query(Basket)
        for row in r:
            db.session.delete(row)
        db.session.commit()


def test_cart_listing_success(client, cleanup_carts, authorization):
    res = client.get('/carts', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_cart_listing_failure(client):
    # 인증 정보를 보내지 않게 해서 요청 실패 유도
    res = client.get('/carts')
    assert res.status_code == 401, res.status_code


def test_cart_add_success(client, authorization):
    for i in range(3):
        res = client.post("/carts", json={
            "goods_code": f"TS{i}",
            "goods_cnt": 1
        }, headers=[authorization])
        assert res.status_code == 200, res.get_json()


def test_cart_add_failure_notfound_goods(client, authorization):
    res = client.post("/carts", json={
        "goods_code": "TS1000",
        "goods_cnt": 1
    }, headers=[authorization])
    assert res.status_code == 400, res.get_json()


def test_cart_add_failure_badinfo(client, authorization):
    res = client.post("/carts", json={
        "goods_code": "T",
        "goods_cnt": 0
    }, headers=[authorization])
    assert res.status_code == 400, res.get_json()


def test_cart_modify_success(client, authorization):
    res = client.put("/carts/TS2", json={
        "goods_cnt": 3
    }, headers=[authorization])

    assert res.status_code == 200, res.get_json()


def test_cart_modify_failure(client, authorization):
    res = client.put("/carts/TS10", json={
        "goods_cnt": 3
    }, headers=[authorization])

    assert res.status_code == 404, res.get_json()

    res = client.put("/carts/TS2", json={
        "goods_cnt": -1
    }, headers=[authorization])

    assert res.status_code == 400, res.get_json()


def test_cart_delete_success(client, authorization):
    res = client.delete("/carts/TS2", json={}, headers=[authorization])

    assert res.status_code == 200, res.get_json()


def test_cart_delete_failure(client, authorization):
    res = client.delete("/carts/TS100", json={}, headers=[authorization])

    assert res.status_code == 404, res.get_json()
