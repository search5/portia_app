def test_login_success(client):
    res = client.patch('/api/login', json={
        'username': 'jiho',
        'password': 'jiho'
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
        'username': 'jiho',
        'password': 'jihos'
    })
    assert res.status_code == 401, res.text

def test_login_not_sendinfo(client):
    res = client.patch('/api/login', json={})
    assert res.status_code == 401, res.text
