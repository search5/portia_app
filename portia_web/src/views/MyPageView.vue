<script>
import {defineComponent} from 'vue'
import TopMenuView from "@/components/TopMenuView.vue";
import FooterView from "@/components/FooterView.vue";
import {http_inst, number_format} from "../lib";
import MyPageSlot from "../components/MyPageSlot.vue";

export default defineComponent({
  name: "MyPageView",
  methods: {number_format},
  data: () => ({
    order_items: []
  }),
  components: {MyPageSlot, FooterView, TopMenuView},
  mounted() {
    http_inst.get('/api/myinfo/orders/latest').then(result => {
      this.order_items = result.data.items
    }).catch(error => {
      alert('최근 구매 정보를 읽어오는데 실패했습니다')
    })
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <MyPageSlot>
      <h3>최근 구매 내역 5건</h3>
      <table class="table table-hover mb-5">
        <thead>
        <tr>
          <th>구매번호</th>
          <th>구매상품</th>
          <th>가격</th>
          <th>구매일</th>
        </tr>
        </thead>
        <tbody>
        <tr :key="index" v-for="(item, index) in order_items">
          <td style="width: 190px;" class="align-middle">{{ item.uuid }}</td>
          <td>
            <img class="img-thumbnail me-2" :src="item.img" style="height: 50px;">
            <RouterLink :to="{ name: 'myorder_detail', params: { uuid: item.uuid } }">{{ item.title }}</RouterLink>
          </td>
          <td class="align-middle">{{ number_format(item.price) }}</td>
          <td class="align-middle">{{ item.order_date }}</td>
        </tr>
        </tbody>
      </table>
    </MyPageSlot>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>