def test_myinfo_get_success(client, authorization):
    res = client.get('/myinfo', headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_myinfo_get_failure(client):
    res = client.get('/myinfo')
    assert res.status_code == 401, res.get_json()


def test_myinfo_modify_success(client, authorization):
    res = client.put('/myinfo', json={}, headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_myinfo_modify_failure_badinfo(client, authorization):
    res = client.put('/myinfo', json={}, headers=[authorization])
    assert res.status_code == 200, res.get_json()


def test_recently_orders_success(client, authorization):
    assert 500 == 200, 'Not Implemented'


def test_all_orders_success(client, authorization):
    assert 500 == 200, 'Not Implemented'


def test_all_orders_failure(client, authorization):
    assert 500 == 200, 'Not Implemented'


def test_order_detail_success(client, authorization):
    assert 500 == 200, 'Not Implemented'


def test_order_detail_failure(client, authorization):
    assert 500 == 200, 'Not Implemented'
