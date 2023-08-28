<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import MyPageSlot from "../components/MyPageSlot.vue";
import {number_format} from "../lib";
import PaginationItem from "../components/PaginationItem.vue";

export default defineComponent({
  name: "MyOrdersView",
  methods: {
    number_format,
    page_move (page_no) {
      this.page_no = page_no

      // TODO Server Call
    }
  },
  components: {PaginationItem, MyPageSlot, TopMenuView, FooterView},
  data: () => ({
    page_no: 1,
    order_items: [
      {
        uuid: 'Portia2023AUG171540',
        title: '잘 나가는 상품 외 1개',
        img: '/api/placeholder/100x50',
        price: 30000,
        order_date: '2023-08-17'
      }
    ]
  })
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <MyPageSlot>
      <h3>전체 구매 내역</h3>
      <table class="table table-hover mb-2">
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
            <img class="img-thumbnail me-2" :src="item.img">
            <RouterLink :to="{ name: 'myorder_detail', params: { uuid: item.uuid } }">{{ item.title }}</RouterLink>
          </td>
          <td class="align-middle">{{ number_format(item.price) }}</td>
          <td class="align-middle">{{ item.order_date }}</td>
        </tr>
        </tbody>
      </table>

      <PaginationItem :page="page_no" :total="10" @page_click="page_move"></PaginationItem>
    </MyPageSlot>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>