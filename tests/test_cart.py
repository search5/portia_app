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
    res = 500
    assert res == 200, "Not Implemented"


def test_cart_add_failure(client):
    authorization = login_auth(client)

    res = 500
    assert res == 200, "Not Implemented"


def test_cart_modify_success(client):
    authorization = login_auth(client)

    res = 500
    assert res == 200, "Not Implemented"


def test_cart_modify_failure(client):
    authorization = login_auth(client)

    res = 500
    assert res == 200, "Not Implemented"


def test_cart_delete_success(client):
    authorization = login_auth(client)

    res = 500
    assert res == 200, "Not Implemented"


def test_cart_delete_failure(client):
    authorization = login_auth(client)

    res = 500
    assert res == 200, "Not Implemented"
