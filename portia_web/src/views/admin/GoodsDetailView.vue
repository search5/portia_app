<script>
import TopMenuView from "../../components/TopMenuView.vue";
import AdminLeftView from "../../components/AdminLeftView.vue";
import FooterView from "../../components/FooterView.vue";
import {http_inst, number_format} from "../../lib";

export default {
  name: "GoodsDetailView",
  methods: {
    number_format,
    delete_goods () {
      if (confirm('정말 삭제하시겠어요?')) {
        http_inst.delete('/api/admin/goods/' + this.$route.params.id + '/delete').then(result => {
          alert('삭제되었습니다')
          this.$router.push({name: 'admin_goods_list', params: {page: 1}})
        }).catch(error => {
          alert('상품 정보를 삭제하던 중 오류가 발생했습니다')
        })
      }
    }
  },
  components: {FooterView, AdminLeftView, TopMenuView},
  data: () => ({
    info: {
      goods_code: '',
      goods_name: '',
      price: '',
      goods_photo_url: '',
      goods_cnt: 0,
      goods_description: '',
      created_date: ''
    }
  }),
  mounted() {
    http_inst.get('/api/admin/goods/' + this.$route.params.id).then(result => {
      Object.assign(this.info, result.data)
    }).catch(error => {
      alert('상품 정보를 불러오던 중 오류가 발생했습니다')
    })
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
          <div class="row">
            <label for="fieldGoodsCode" class="form-label col-form-label col-2">상품 코드</label>
            <div class="col-10">
              <input type="text" class="form-control form-control-plaintext" readonly id="fieldGoodsCode" v-model="info.goods_code">
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <label for="fieldGoodsName" class="form-label col-form-label col-2">상품명</label>
            <div class="col-10">
              <input type="text" class="form-control form-control-plaintext" readonly id="fieldGoodsName" v-model="info.goods_name">
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <label for="fieldGoodsPrice" class="form-label col-form-label col-2">가격</label>
            <div class="col-10">
              <input type="text" class="form-control form-control-plaintext" readonly id="fieldGoodsPrice" v-model="info.price">
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <label for="fieldGoodsPhoto" class="form-label col-form-label col-2">사진</label>
            <div class="col-10">
              <img class="img-fluid" :src="info.goods_photo_url" style="height: 300px;">
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <label for="fieldGoodsCnt" class="form-label col-form-label col-2">재고</label>
            <div class="col-10">
              <input type="number" class="form-control form-control-plaintext" readonly id="fieldGoodsCnt" v-model="info.goods_cnt">
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <label for="fieldGoodsDescription" class="form-label col-form-label col-2">설명</label>
            <div class="col-10">
              <textarea class="form-control" id="fieldGoodsDescription form-control-plaintext" rows="3" readonly v-model="info.goods_description"></textarea>
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <label for="fieldGoodsCreated" class="form-label col-form-label col-2">등록일자</label>
            <div class="col-10">
              <input type="text" class="form-control form-control-plaintext" readonly id="fieldGoodsCreated" v-model="info.created_date">
            </div>
          </div>
        </div>
        <RouterLink class="btn btn-primary me-2" :to="{name: 'admin_goods_list', params: {page: 1}}">목록으로</RouterLink>
        <RouterLink class="btn btn-success me-2" :to="{name: 'admin_goods_register'}">새로 등록</RouterLink>
        <RouterLink class="btn btn-warning me-2" :to="{name: 'admin_goods_modify', params: {id: $route.params.id}}">수정하기</RouterLink>
        <button class="btn btn-danger me-2" @click="delete_goods">삭제하기</button>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>