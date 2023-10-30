def test_placeholder_success(client):
    res = client.get('/api/placeholder/100x100')
    assert res.status_code == 200, res.text

def test_placeholder_failure(client):
    res = client.get('/api/placeholder/100i100')
    assert res.status_code == 200, res.text