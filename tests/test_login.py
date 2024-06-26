import time


def test_login_success(client):
    res = client.patch('/api/login', json={
        'username': 'admin@portia.shop',
        'password': 'admin'
    })
    assert res.status_code == 200, res.text


def test_login_failure_badname(client):
    res = client.patch("/api/login", json={
        'username': 'jiho1',
        'password': 'jiho'
    })
    assert res.status_code == 401, res.text


def test_login_failure_badpassword(client):
    res = client.patch('/api/login', json={
        'username': 'admin@portia.shop',
        'password': 'jihos'
    })
    assert res.status_code == 401, res.text


def test_login_not_sendinfo(client):
    res = client.patch('/api/login', json={})
    assert res.status_code == 401, res.text


def test_login_not_sendinfo2(client):
    res = client.patch('/api/login', json={
        'username': '',
        'password': ''
    })
    assert res.status_code == 400, res.text


def test_logout(client):
    res = client.patch('/api/login', json={
        'username': 'admin@portia.shop',
        'password': 'admin'
    })
    assert res.status_code == 200, res.text

    assert 'access_token' in res.get_json(), res.get_json()
    authorization = f"Bearer {res.get_json()['access_token']}"

    res = client.get('/api/logout', headers=[("Authorization", authorization)])
    assert res.status_code == 302, res.text

