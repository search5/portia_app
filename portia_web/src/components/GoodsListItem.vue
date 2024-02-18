<script>
import {number_format} from "../lib";
import axios from "axios";
import PaginationItem from "./PaginationItem.vue";

export default {
  name: "GoodsListItem",
  components: {PaginationItem},
  props: ['limit'],
  data: () => ({
    goods: [],
    goods_total_page: 1
  }),
  methods: {
    number_format,
    page_move (page_no) {
      this.$router.push({name: 'goods_list', query: {page: page_no}})

      this.load_list(page_no)
    },
    load_list (page) {
      // 서버에 상품 리스트 API 호출한 것을 goods 변수에 담아둔다.
      let api_request = null
      if (this.limit !== undefined) {
        api_request = axios.get('/api/goods', {
          params: { limit: this.limit }
        })
      } else {
        api_request = axios.get('/api/goods', {
          params: { page: page }
        })
      }

      api_request.then(result => {
        this.goods = result.data.data.items
        this.goods_total_page = Math.ceil(result.data.data.total / result.data.data.per_page)
      }).catch(error => {
        alert('상품 목록을 불러오던 중 오류가 발생했습니다')
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
  mounted() {
    this.load_list(this.page_value)
  }
}
</script>

<template>
  <div>
    <div class="row">
      <div class="col-lg-4 col-md-6 mb-4" :key="index" v-for="(item, index) in goods">
        <div class="card h-100">
          <a href="#"><img class="card-img-top" :src="item.goods_photo_url" alt="" style="height: 233px;"></a>
          <div class="card-body">
            <h4 class="card-title">
              <RouterLink :to="{name: 'goods_view', params: {id: item.goods_code}}">{{ item.goods_name }}</RouterLink>
            </h4>
            <h5>{{ number_format(item.price) }}</h5>
            <p class="card-text">{{ item.goods_description }}</p>
          </div>
          <div class="card-footer"></div>
        </div>
      </div>
    </div>
    <div class="row" v-if="this.limit === undefined">
      <PaginationItem :page="page_value" :total="goods_total_page" @page_click="page_move"></PaginationItem>
    </div>
  </div>
</template>

<style scoped>

</style>