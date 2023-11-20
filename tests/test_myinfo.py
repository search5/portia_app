def test_myinfo_get_success(client, authorization):
    res = client.get('/myinfo', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_myinfo_get_failure(client):
    res = client.get('/myinfo')
    assert res.status_code == 401, res.get_json()


def test_myinfo_modify_success(client, second_authorization):
    res = client.put('/myinfo', json={
        "name": "홍길동",
        "password": "jiho1",
        "email": "gdhong@gmail.com"
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
    res = client.get('/myinfo/order-latest', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_all_orders_success(client, authorization):
    res = client.get('/myinfo/orders', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_all_orders_failure(client, authorization):
    res = client.get('/myinfo/orders?page=alpha', headers=[authorization])
    assert res.status_code == 400, res.get_json()


def test_order_detail_success(client, authorization):
    res = client.get('/myinfo/orders/TS10', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_order_detail_failure(client, authorization):
    res = client.get('/myinfo/orders/TS10')
    assert res.status_code == 401, res.get_json()

    res = client.get('/myinfo/orders/TS11', headers=[authorization])
    assert res.status_code == 400, res.get_json()
