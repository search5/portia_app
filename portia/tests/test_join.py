import pytest


@pytest.fixture()
def cleanup_success():
    from portia.models import DeliveryAddresses, db, User
    from portia.main import app

    # success data clean
    with app.app_context():
        r = db.session.query(DeliveryAddresses).filter(DeliveryAddresses.username == 'search5@gmail.com').first()
        if r:
            db.session.delete(r)

        r = db.session.query(User).filter(User.username == 'search5@gmail.com').first()
        if r:
            db.session.delete(r)

        db.session.commit()


def test_join_success(client, cleanup_success):
    # cleanup_success
    res = client.post("/api/users/join", json={
        'real_name': '이지호',
        'real_email': 'search5@gmail.com',
        'user_password': 'dmsthfl',
        'post_code': '10346',
        'addresses': '경기도 고양시 일산서구',
        'detail_address': '일청로 91번길'
    })
    assert res.status_code == 200, res.text


def test_join_failure_duplicate(client, cleanup_success):
    # cleanup_success
    send_data={
        'real_name': '이지호',
        'real_email': 'search5@gmail.com',
        'user_password': 'dmsthfl',
        'post_code': '10346',
        'addresses': '경기도 고양시 일산서구',
        'detail_address': '일청로 91번길'
    }

    res = client.post("/api/users/join", json=send_data)
    assert res.status_code == 200, res.text

    res = client.post("/api/users/join", json=send_data)
    assert res.status_code == 400, res.text


def test_join_failed_validate(client):
    res = client.post("/api/users/join", json={
        'real_name': '이지호',
        'real_email': 'search5',
        'user_password': 'dmsthfl',
        'post_code': '10346',
        'addresses': '경기도 고양시 일산서구',
        'detail_address': '일청로 91번길'
    })
    assert res.status_code == 400, res.text

