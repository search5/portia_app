import pytest

from portia.main import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def admin_authorization(client):
    res = client.patch('/api/login', json={
        'username': 'admin@portia.shop',
        'password': 'admin'
    })
    assert res.status_code == 200, res.text

    authorization = f"Bearer {res.get_json()['access_token']}"

    return "Authorization", authorization


@pytest.fixture()
def authorization(client):
    res = client.patch('/api/login', json={
        'username': 'user@portia.shop',
        'password': 'user'
    })
    assert res.status_code == 200, res.text

    authorization = f"Bearer {res.get_json()['access_token']}"

    return "Authorization", authorization


@pytest.fixture()
def second_authorization(client):
    res = client.patch('/api/login', json={
        'username': 'gdhong@portia.shop',
        'password': 'gdhong'
    })
    assert res.status_code == 200, res.text

    authorization = f"Bearer {res.get_json()['access_token']}"

    return "Authorization", authorization
