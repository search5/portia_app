<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import MyPageSlot from "../components/MyPageSlot.vue";

export default defineComponent({
  name: "MyOrderDetail",
  components: {MyPageSlot, TopMenuView, FooterView}
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <MyPageSlot>
      <div class="row">
        <div class="col-3"><strong>구매번호</strong></div>
        <div class="col"></div>
        <div class="col-3"><strong>구매일</strong></div>
        <div class="col"></div>
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
            <tr>
              <td>1</td>
              <td>1</td>
              <td>1</td>
              <td>1</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="row">
        <div class="col-2">결제 총 금액</div>
        <div class="col">10,000</div>
      </div>
      <div class="row mb-3">
        <div class="col-2">결제 상태</div>
        <div class="col">결제중|결제취소|결제완료|입금대기|입금완료</div>
      </div>

      <h4>주문자 정보</h4>
      <div class="row mt-2 mb-3">
        <div class="col-2">이름</div>
        <div class="col"></div>
        <div class="col-2">연락처</div>
        <div class="col"></div>
      </div>

      <h4>배송지 정보</h4>
      <div class="row mt-2">
        <div class="col-2">이름</div>
        <div class="col"></div>
        <div class="col-2">연락처</div>
        <div class="col"></div>
      </div>
      <div class="row mt-2 mb-4">
        <div class="col-2">배송지 주소</div>
        <div class="col"></div>
      </div>
    </MyPageSlot>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>