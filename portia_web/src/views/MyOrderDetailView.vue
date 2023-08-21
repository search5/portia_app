<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import MyPageSlot from "../components/MyPageSlot.vue";
import {number_format} from "../lib";

export default defineComponent({
  name: "MyOrderDetail",
  methods: {number_format},
  components: {MyPageSlot, TopMenuView, FooterView},
  data: () => ({
    order_no: 'ABCD',
    order_date: '2023-08-21',
    items: [
      {
        goods_name: '상품 1',
        goods_cnt: 2,
        goods_price: 30000,
        goods_total_price: 60000,
      }
    ],
    orderers: {
      name: '홍길동',
      phone: '010-1234-5678'
    },
    ship_to: {
      name: '홍길동',
      phone: '010-1234-5678',
      addresses: '경기도 고양시 일산서구 일청로',
      post_code: '10236'
    },
    order_status: '결제중' // 결제중|결제취소|결제완료|입금대기|입금완료
  }),
  computed: {
    total_price () {
      return 0
    }
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <MyPageSlot>
      <div class="row">
        <div class="col-3"><strong>구매번호</strong></div>
        <div class="col">{{ order_no }}</div>
        <div class="col-3"><strong>구매일</strong></div>
        <div class="col">{{ order_date }}</div>
      </div>
      <div class="row mt-2">
        <div class="col">
          <table class="table table-bordered table-hover">
            <thead>
            <tr>
              <th>상품정보</th>
              <th>개수</th>
              <th>가격</th>
              <th>전체 가격</th>
            </tr>
            </thead>
            <tbody>
            <tr :key="index" v-for="(item, index) in items">
              <td>{{ item.goods_name }}</td>
              <td>{{ item.goods_cnt }}</td>
              <td>{{ number_format(item.goods_price) }}</td>
              <td>{{ number_format(item.goods_total_price) }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="row">
        <div class="col-2">결제 총 금액</div>
        <div class="col">{{ number_format((total_price)) }}</div>
      </div>
      <div class="row mb-3">
        <div class="col-2">결제 상태</div>
        <div class="col">{{ order_status }}</div>
      </div>

      <h4>주문자 정보</h4>
      <div class="row mt-2 mb-3">
        <div class="col-1">이름</div>
        <div class="col-1">{{ orderers.name }}</div>
        <div class="col-2">연락처</div>
        <div class="col">{{ orderers.phone }}</div>
      </div>

      <h4>배송지 정보</h4>
      <div class="row mt-2">
        <div class="col-1">이름</div>
        <div class="col-1">{{ ship_to.name }}</div>
        <div class="col-2">연락처</div>
        <div class="col">{{ ship_to.phone }}</div>
      </div>
      <div class="row mt-2 mb-4">
        <div class="col-1">우편번호</div>
        <div class="col-1">{{ ship_to.post_code }}</div>
        <div class="col-2">배송지 주소</div>
        <div class="col">{{ ship_to.addresses }}</div>
      </div>
    </MyPageSlot>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>