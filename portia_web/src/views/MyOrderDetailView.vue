<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import MyPageSlot from "../components/MyPageSlot.vue";
import {http_inst, number_format} from "../lib";
import {forEach} from "lodash-es";

export default defineComponent({
  name: "MyOrderDetail",
  methods: {number_format},
  components: {MyPageSlot, TopMenuView, FooterView},
  data: () => ({
    order_no: '',
    order_date: '',
    items: [],
    orderers: {
      name: '',
      phone: ''
    },
    ship_to: {
      name: '',
      phone: '',
      addresses: '',
      post_code: ''
    },
    order_status: ''
  }),
  computed: {
    total_price () {
      let total_value = 0

      forEach(this.items, (value) => {
        total_value += value.goods_total_price
      });

      return total_value
    }
  },
  mounted() {
    const order_id = this.$route.params.uuid
    http_inst.get('/api/myinfo/orders/' + order_id).then(result => {
      const order_data = result.data.data
      this.order_date = order_data.order_date
      this.order_no = order_data.order_no
      this.order_status = order_data.order_status

      Object.assign(this.items, order_data.items)
      Object.assign(this.orderers, order_data.orderers)
      Object.assign(this.ship_to, order_data.ship_to)
    }).catch(error => {
      alert('구매 정보를 읽어오는데 실패했습니다')
    })
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