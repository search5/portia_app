<script>
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import {http_inst, number_format} from "@/lib";
import {forEach} from "lodash-es";

export default {
  name: "PaymentView",
  components: {TopMenuView, FooterView},
  data: () => ({
    cart_items: [],
    sender: {
      name: '',
      phone: ''
    },
    receiver: {
      name: '',
      phone: '',
      post: '',
      addr: ''
    },
    payment_method: 'bank'
  }),
  methods: {
    number_format,
    payment_process () {
      alert('결제를 진행합니다')
      // TODO
      // 0. 그 전에 백엔드쪽 기능을 살펴봐야 한다.
      // 1. DB에 집어넣는다.
      // 2. 주문이 완료되었음을 알리고 내 주문 목록으로 이동한다.
    }
  },
  computed: {
    total_money () {
      let total_value = 0

      forEach(this.cart_items, (value) => {
        total_value += value.price * value.cart_cnt
      });

      return total_value
    }
  },
  mounted () {
    http_inst.get('/api/carts').then(result => {
      const response_data = result.data
      this.cart_items = response_data.data
    }).catch(error => {
      alert('장바구니 정보를 불러오는데 실패했습니다')
    })
  }
}
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container mb-3">
      <div class="card shopping-cart">
        <div class="card-header bg-dark text-light">
          <font-awesome-icon icon="fa-solid fa-shopping-cart" />
          결제하기
          <div class="clearfix"></div>
        </div>
        <div class="card-body">
          <!-- PRODUCT -->
          <table class="table table-hover table-striped">
            <thead>
            <tr>
              <th style="width: 120px;"></th>
              <th>상품명</th>
              <th>단가</th>
              <th>수량</th>
              <th>가격</th>
            </tr>
            </thead>
            <tfoot>
            <tr>
              <td colspan="5" class="text-end">Total price: <b>{{ number_format(total_money) }}</b></td>
            </tr>
            </tfoot>
            <tbody>
            <tr :key="index" v-for="(item, index) in cart_items">
              <td><img class="img-responsive" :src="item.goods_photo_url" alt="preview" width="120" height="80"></td>
              <td>{{ item.goods_name }}<br><small>{{ item.goods_description }}</small></td>
              <td>{{ number_format(item.price) }}</td>
              <td>{{ item.cart_cnt }}</td>
              <td>{{ number_format(item.price * item.cart_cnt) }}</td>
            </tr>
            </tbody>
          </table>

          <hr class="mt-4 mb-4">
          <!-- 구매자 -->
          <h3>구매자 정보</h3>
          <div class="row">
            <div class="col">
              <div class="row mb-3">
                <label for="sender_name" class="col-form-label col-3">이름</label>
                <div class="col-9">
                  <input type="text" class="form-control" id="sender_name" v-model="sender.name">
                </div>
              </div>
            </div>
            <div class="col">
              <div class="row mb-3">
                <label for="sender_phone" class="col-form-label col-3">전화번호</label>
                <div class="col-9">
                  <input type="text" class="form-control" id="sender_phone" v-model="sender.phone">
                </div>
              </div>
            </div>
          </div>

          <hr class="mt-4 mb-4">

          <!-- 배송지 -->
          <h3>배송지 정보</h3>

          <div class="row">
            <div class="col">
              <div class="row mb-3">
                <label for="received_name" class="col-form-label col-3">이름</label>
                <div class="col-9">
                  <input type="text" class="form-control" id="received_name" v-model="receiver.name">
                </div>
              </div>
            </div>
            <div class="col">
              <div class="row mb-3">
                <label for="received_phone" class="col-form-label col-3">전화번호</label>
                <div class="col-9">
                  <input type="text" class="form-control" id="received_phone" v-model="receiver.phone">
                </div>
              </div>
            </div>
          </div>
          <div class="row mb-3">
            <label for="received_post" class="col-form-label col-2">우편번호</label>
            <div class="col-10">
              <input type="text" class="form-control" id="received_post" v-model="receiver.post">
            </div>
          </div>
          <div class="row mb-3">
            <label for="received_addr" class="col-form-label col-2">주소</label>
            <div class="col-10">
              <input type="text" class="form-control" id="received_addr" v-model="receiver.addr">
            </div>
          </div>

          <hr class="mt-4 mb-4">

          <!-- 결제 방법 -->
          <h3>결제 방법</h3>

          <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input type="radio" class="btn-check" name="btnpayment" id="btnpaymentbank" autocomplete="off" value="bank" v-model="payment_method">
            <label class="btn btn-outline-primary" for="btnpaymentbank">무통장 입금</label>

            <input type="radio" class="btn-check" name="btnpayment" id="btnpaymentcard" autocomplete="off" value="card" v-model="payment_method">
            <label class="btn btn-outline-primary" for="btnpaymentcard">신용카드</label>

            <input type="radio" class="btn-check" name="btnpayment" id="btnpaymentapp" autocomplete="off" value="app" v-model="payment_method">
            <label class="btn btn-outline-primary" for="btnpaymentapp">앱 결제</label>
          </div>
        </div>

        <div class="card-footer">
          <div class="fa-pull-right" style="margin: 10px">
            <button class="btn btn-success" @click="payment_process">결제 진행</button>
          </div>
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>