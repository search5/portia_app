def test_order_success(client, authorization):
    res = client.post('/api/orders', json={
        "items": [
            {
                "goods_code": 'TS1',
                "goods_cnt": 2,
                "goods_price": 30000
            }
        ],
        "ship_to": {
            "name": "홍길석",
            "phone": "010-1245-7896",
            "addresses": "경기도 양청시 고려동 301",
            "post_code": "10346"
        }
    }, headers=[authorization])
    assert res.status_code == 200, res.text


def test_order_failure(client, authorization):
    # Empty Authorization
    res = client.post('/api/orders', json={})
    assert res.status_code == 401, res.text

    # Bad Request(Empty Field)
    res = client.post('/api/orders', json={
        "items": [],
        "ship_to": {
            "name": "",
            "phone": "",
            "addresses": "",
            "post_code": ""
        }
    }, headers=[authorization])
    assert res.status_code == 400, res.text

    # Bad Request(Bad Data)
    res = client.post('/api/orders', json={
        "items": [
            {
                "goods_code": 'TS0',
                "goods_cnt": 2,
                "goods_price": 30000
            }
        ],
        "ship_to": {
            "name": "홍",
            "phone": "010-1245-7896",
            "addresses": "경기도",
            "post_code": "103"
        }
    }, headers=[authorization])
    assert res.status_code == 400, res.text
