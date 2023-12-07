def test_goods_list_success(client):
    # 등록된 상품 목록 반환 기능
    res = client.get("/api/goods")
    assert res.status_code == 200, res.text


def test_goods_list_failure(client):
    # 등록된 상품 목록 반환 기능(실패 가정)
    res = client.get("/api/goods?page=alpha")
    assert res.status_code == 400, res.text


def test_goods_list_success_query_str(client):
    # 등록된 상품 목록 반환 기능(keyword 전달)
    res = client.get("/api/goods?keyword=TS")
    assert res.status_code == 200, res.text


def test_goods_get_success(client):
    # 등록된 상품의 상세 정보 가져오기
    res = client.get('/api/goods/TS0')
    assert res.status_code == 200, res.text


def test_goods_get_failure_bad_code(client):
    # 등록되어 있지 않은 상품 정보 요청
    res = client.get('/api/goods/alpha')
    assert res.status_code == 404, res.text
