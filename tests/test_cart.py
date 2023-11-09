def login_auth(client):
    res = client.patch('/api/login', json={
        'username': 'jiho',
        'password': 'jiho'
    })
    assert res.status_code == 200, res.text

    authorization = f"Bearer {res.get_json()['access_token']}"

    return "Authorization", authorization


def test_cart_listing_success(client):
    authorization = login_auth(client)

    res = client.get('/carts', headers=[authorization])
    assert res.status_code == 200, res.text


def test_cart_listing_failure(client):
    # 인증 정보를 보내지 않게 해서 요청 실패 유도
    res = client.get('/carts')
    assert res.status_code == 400, res.status_code


def test_cart_add_success(client):
    authorization = login_auth(client)

    for i in range(3):
        res = client.post("/carts/add", json={
            "goods_code": f"TG{i}",
            "goods_cnt": 1
        }, headers=[authorization])
        assert res.status_code == 200, res.text


def test_cart_add_failure(client):
    authorization = login_auth(client)

    res = client.post("/carts/add", json={
        "goods_code": "TG1000",
        "goods_cnt": 1
    }, headers=[authorization])
    assert res.status_code == 400, res.text


def test_cart_modify_success(client):
    authorization = login_auth(client)

    res = client.put("/carts/TG2", json={
        "goods_cnt": 3
    }, headers=[authorization])

    assert res.status_code == 200, res.text


def test_cart_modify_failure(client):
    authorization = login_auth(client)

    res = client.put("/carts/TG10", json={
        "goods_cnt": 3
    }, headers=[authorization])

    assert res.status_code == 404, res.text

    res = client.put("/carts/TG2", json={
        "goods_cnt": -1
    }, headers=[authorization])

    assert res.status_code == 400, res.text


def test_cart_delete_success(client):
    authorization = login_auth(client)

    res = client.delete("/carts/TG2", json={}, headers=[authorization])

    assert res.status_code == 200, res.text


def test_cart_delete_failure(client):
    authorization = login_auth(client)

    res = client.delete("/carts/TG100", json={}, headers=[authorization])

    assert res.status_code == 404, res.text
