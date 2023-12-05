def test_myinfo_get_success(client, authorization):
    res = client.get('/myinfo', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_myinfo_get_failure(client):
    res = client.get('/myinfo')
    assert res.status_code == 401, res.get_json()


def test_myinfo_modify_success(client, second_authorization):
    res = client.put('/myinfo', json={
        "real_name": "홍길동",
        "real_email": "gdhong@portia.shop",
        "user_current_password": "gdhong",
        "user_new_password": "gdhong",
        "user_new_password_confirm": "gdhong",
        "post_code": "10346",
        "addresses": "서울특별시 강서구 염창동",
        "detail_address": "821-40"
    }, headers=[second_authorization])
    assert res.status_code == 200, res.get_json()


def test_myinfo_modify_failure_badinfo(client, second_authorization):
    res = client.put('/myinfo', json={
        "name": "",
        "password": "",
        "email": ""
    }, headers=[second_authorization])
    assert res.status_code == 400, res.get_json()


def test_recently_orders_success(client, authorization):
    res = client.get('/myinfo/orders/latest', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_all_orders_success(client, authorization):
    res = client.get('/myinfo/orders', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_all_orders_failure(client, authorization):
    res = client.get('/myinfo/orders?page=alpha', headers=[authorization])
    assert res.status_code == 400, res.get_json()


def test_order_detail_success(client, authorization):
    res = client.get('/myinfo/orders/7777578724', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_order_detail_failure(client, authorization):
    res = client.get('/myinfo/orders/677278653', headers=[authorization])
    assert res.status_code == 404, res.get_json()

    res = client.get('/myinfo/orders/TS10')
    assert res.status_code == 401, res.get_json()

