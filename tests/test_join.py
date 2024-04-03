import pytest


@pytest.fixture()
def cleanup_login():
    from portia.models import DeliveryAddresses, db, User
    from portia.main import app

    # success data clean
    with app.app_context():
        db.session.execute(db.delete(DeliveryAddresses).where(DeliveryAddresses.username == 'gdhong@gmail.com'))
        db.session.execute(db.delete(User).where(User.username == 'gdhong@gmail.com'))
        db.session.commit()


def test_join_success(client, cleanup_login):
    # cleanup_success
    res = client.post("/api/users/join", json={
        'real_name': 'gil-dong',
        'real_email': 'gdhong@gmail.com',
        'user_password': 'iiii',
        'post_code': '10346',
        'addresses': '경기도 양청시 일산북구',
        'detail_address': '일백로 42번길',
        'phone': '010-1234-5678'
    })
    assert res.status_code == 200, res.text


def test_join_failure_duplicate(client, cleanup_login):
    # cleanup_success
    send_data = {
        'real_name': 'gil-dong',
        'real_email': 'gdhong@gmail.com',
        'user_password': 'iiii',
        'post_code': '10346',
        'addresses': '경기도 양청시 일산북구',
        'detail_address': '일백로 42번길',
        'phone': '010-1234-5678'
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
        'detail_address': '일청로 91번길',
        'phone': '010-1234-5678'
    })
    assert res.status_code == 400, res.text
