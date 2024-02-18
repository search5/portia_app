<script>
import TopMenuView from "../../components/TopMenuView.vue";
import AdminLeftView from "../../components/AdminLeftView.vue";
import FooterView from "../../components/FooterView.vue";
import {http_inst} from "../../lib";

export default {
  name: "GoodsRegisterView",
  components: {FooterView, AdminLeftView, TopMenuView},
  data: () => ({
    info: {
      goods_name: '',
      price: '',
      goods_file: '',
      goods_cnt: 0,
      goods_description: '',
      created_date: ''
    }
  }),
  methods: {
    goods_register () {
      http_inst.post("/api/admin/goods/register", {
        'goods_name': this.info.goods_name,
        'price': this.info.price,
        'goods_cnt': this.info.goods_cnt,
        'goods_description': this.info.goods_description
      }).then(result => {
        const post_data = new FormData()
        post_data.append('goods_photo', this.info.goods_file)

        http_inst.post('/api/admin/goods/' + result.data.goods_code + '/upload', post_data, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        // 상품 목록 페이지로 이동
        this.$router.push({name: 'admin_goods_list'})
      }).catch(error => {
        alert('상품 등록 중 오류가 발생했습니다')
      })
    },
    onChangedFile (event) {
      this.info.goods_file = event.target.files[0]
    }
  }
}
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="d-flex flex-row flex-shrink-0 p-3 bg-body-tertiary">
      <AdminLeftView></AdminLeftView>

      <div class="container">
        <div class="mb-3">
          <label for="fieldGoodsName" class="form-label">상품명</label>
          <input type="text" class="form-control" id="fieldGoodsName" v-model="info.goods_name">
        </div>
        <div class="mb-3">
          <label for="fieldGoodsPrice" class="form-label">가격</label>
          <input type="number" class="form-control" id="fieldGoodsPrice" v-model="info.price">
        </div>
        <div class="mb-3">
          <label for="fieldGoodsPhoto" class="form-label">사진</label>
          <input type="file" class="form-control" id="fieldGoodsPhoto" @change="onChangedFile">
        </div>
        <div class="mb-3">
          <label for="fieldGoodsCnt" class="form-label">재고</label>
          <input type="number" class="form-control" id="fieldGoodsCnt" v-model="info.goods_cnt">
        </div>
        <div class="mb-3">
          <label for="fieldGoodsDescription" class="form-label">설명</label>
          <textarea class="form-control" id="fieldGoodsDescription" rows="3" v-model="info.goods_description"></textarea>
        </div>

        <button class="btn btn-primary me-2" @click="goods_register">등록하기</button>
        <RouterLink class="btn btn-success me-2" :to="{name: 'admin_goods_list', params: {page: 1}}">취소하기</RouterLink>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>