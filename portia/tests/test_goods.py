import pytest


@pytest.fixture()
def cleanup_goods(client):
    pass


def test_goods_register_success(client):
    # 상품 등록 기능
    res = client.post("/admin/goods/register", json={
        'goods_name': '상품 1',
        'price': 30000,
        'goods_cnt': 1,
        'goods_description': '상품 등록 테스트'
    })
    assert res.status_code == 200, res.status_code


def test_goods_register_notsend_failure(client):
    # 상품 등록 기능
    res = client.post("/admin/goods/register", json={})
    assert res.status_code == 400, res.status_code


def test_goods_register_failure(client):
    # 상품 등록 기능
    # res = client.post("/admin/goods/register", json={})
    # assert res.status_code == 200, res.status_code
    assert 100 == 200


def test_goods_modify_success(client):
    # 상품 수정 기능
    res = client.put("/admin/goods/1/modify", json={})
    assert res.status_code == 200, res.status_code


def test_goods_modify_failure(client):
    # 상품 수정 기능
    res = client.put("/admin/goods/1/modify", json={})
    assert res.status_code == 200, res.status_code


def test_goods_delete_success(client):
    # 상품 삭제 기능
    res = client.delete("/admin/goods/1/delete", json={})
    assert res.status_code == 200, res.status_code


def test_goods_delete_failure(client):
    # 상품 삭제 기능
    res = client.delete("/admin/goods/1/delete", json={})
    assert res.status_code == 200, res.status_code


def test_goods_list_success(client):
    # 등록된 상품 목록 반환 기능
    res = client.get("/admin/goods", json={})
    assert res.status_code == 200, res.status_code


def test_goods_list_failure(client):
    # 등록된 상품 목록 반환 기능
    res = client.get("/admin/goods", json={})
    assert res.status_code == 200, res.status_code
