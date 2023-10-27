from portia.factory import create_app


def test_login_call(client):
    res = client.patch('/api/login', json={
        'username': 'jiho1',
        'password': 'jiho'
    })
    print(res.headers)
    print(res.request.headers)
    # print(dir(res.request))
    # print(res.request.get_data())
    # print(res.request.get_json())
    assert res.status_code == 200, res.text
