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

# TODO
# 최근 5건 주문 정보
# 전체 주문 정보(페이징 기능 추가)
# 업로드된 상품 이미지를 서비스할 수 있는 기능 및 테스트 필요
# 주문 상세 테이블에 아래 항목 추가 필요...(하다보니 늘어나네)
# ship_to: {
#       name: '홍길동',
#       phone: '010-1234-5678',
#       addresses: '경기도 고양시 일산서구 일청로',
#       post_code: '10236'
#     },
#     order_status: '결제중' // 결제중|결제취소|결제완료|입금대기|입금완료
# OrdersView.vue 만들어야 함
