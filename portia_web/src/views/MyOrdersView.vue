<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import MyPageSlot from "../components/MyPageSlot.vue";
import {http_inst, number_format} from "../lib";
import PaginationItem from "../components/PaginationItem.vue";

export default defineComponent({
  name: "MyOrdersView",
  methods: {
    number_format,
    page_move (page_no) {
      this.$router.push({name: 'myorder', query: {page: page_no}})

      http_inst.get('/api/myinfo/orders', {params: {page: page_no}}).then(result => {
        this.order_items = result.data.data.items
        this.total_page = Math.ceil(result.data.data.total / result.data.data.per_page)
      }).catch(error => {
        alert('전체 구매 정보를 읽어오는데 실패했습니다')
      })
    }
  },
  components: {PaginationItem, MyPageSlot, TopMenuView, FooterView},
  data: () => ({
    order_items: [],
    total_page: 1
  }),
  mounted() {
    this.page_move(1)
  }
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
            <img class="img-thumbnail me-2" :src="item.img" style="height: 50px;">
            <RouterLink :to="{ name: 'myorder_detail', params: { uuid: item.uuid } }">{{ item.title }}</RouterLink>
          </td>
          <td class="align-middle">{{ number_format(item.price) }}</td>
          <td class="align-middle">{{ item.order_date }}</td>
        </tr>
        </tbody>
      </table>

      <PaginationItem :page="parseInt($route.query.page)" :total="total_page" @page_click="page_move"></PaginationItem>
    </MyPageSlot>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>