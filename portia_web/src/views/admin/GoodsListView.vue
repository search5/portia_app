<script>
import PaginationItem from "../../components/PaginationItem.vue";
import AdminLeftView from "../../components/AdminLeftView.vue";
import FooterView from "../../components/FooterView.vue";
import TopMenuView from "../../components/TopMenuView.vue";
import {http_inst, number_format} from "../../lib";

export default {
  name: "GoodsListView",
  components: {TopMenuView, FooterView, AdminLeftView, PaginationItem},
  data: () => ({
    items: [],
    total_page: 2
  }),
  methods: {
    number_format,
    page_move (page_no) {
      this.$router.push({
        name: 'admin_goods_list',
        query: {
          page: page_no
        }
      })

      http_inst.get("/api/admin/goods", {
        params: { page: page_no }
      }).then(result => {
        const resp_data = result.data
        Object.assign(this.items, resp_data.data.items)
        this.total_page = Math.ceil(resp_data.data.total / resp_data.data.per_page)
      }).catch(error => {
        alert('등록된 상품 리스트를 불러오는 도중 오류가 발생했습니다')
      })
    }
  },
  computed: {
    page_value () {
      if (this.$route.query.page !== undefined) {
        return parseInt(this.$route.query.page)
      } else {
        return 1
      }
    }
  },
  mounted () {
    this.page_move(1)
  }
}
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="d-flex flex-row flex-shrink-0 p-3 bg-body-tertiary">
      <AdminLeftView></AdminLeftView>

      <div class="container mt-3">
        <h3>상품 목록</h3>
        <table class="table table-bordered table-hover">
          <thead>
          <tr>
            <th style="width: 20%;">상품 코드</th>
            <th style="width: 40%;">상품명</th>
            <th>가격</th>
            <th>재고</th>
            <th>등록일</th>
          </tr>
          </thead>
          <tbody>
          <tr :key="index" v-for="(item, index) in items">
            <td>{{ item.goods_code }}</td>
            <td>
              <RouterLink :to="{name: 'admin_goods_view', params: {
                id: item.goods_code
              }}">{{ item.goods_name }}</RouterLink>
            </td>
            <td>{{ number_format(item.price) }}</td>
            <td>{{ item.goods_cnt }}</td>
            <td>{{ item.created_date }}</td>
          </tr>
          </tbody>
        </table>

        <PaginationItem :page="page_value" :total="total_page" @page_click="page_move"></PaginationItem>

        <RouterLink :to="{name: 'admin_goods_register'}" class="btn btn-primary">상품 추가</RouterLink>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>