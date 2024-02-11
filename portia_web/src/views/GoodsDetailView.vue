<script>
import {defineComponent} from 'vue'
import FooterView from "../components/FooterView.vue";
import TopMenuView from "../components/TopMenuView.vue";
import {range} from "lodash-es";
import {http_inst, number_format} from "../lib";
import axios from "axios";

export default defineComponent({
  name: "GoodsDetailView",
  components: {FooterView, TopMenuView},
  data: () => ({
    item: {
      goods_code: -1,
      goods_photo_url: '',
      goods_name: '',
      price: 0,
      goods_description: ''
    },
    quantity: 1
  }),
  methods: {
    number_format,
    range,
    basket_add () {
      http_inst.post("/api/carts", {
          "goods_code": this.item.goods_code,
          "goods_cnt": this.quantity
      }).then(result => {
        alert('[' + this.item.goods_name + '] ' + this.quantity + '개를 장바구니에 담았습니다')
      }).catch(error => {
        alert('상품을 장바구니에 담던 중 오류가 발생했습니다')
      })
    }
  },
  mounted() {
    const goods_code = this.$route.params.id

    axios.get('/api/goods/' + goods_code).then(result => {
      this.item = result.data
    }).catch(error => {
      alert('상품 정보를 받아오던 중 오류가 발생했습니다')
    })
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container">
      <div class="row">
        <div class="col-12">
          <form>
            <input type="hidden" name="goods_id" value="{ item.goods_code }">
            <div class="card mb-4">
              <div class="row">
                <aside class="col-sm-5 border-right">
                  <article class="gallery-wrap">
                    <div class="img-big-wrap">
                      <div>
                        <img :src="item.goods_photo_url" class="img-fluid">
                      </div>
                    </div> <!-- slider-product.// -->
                  </article> <!-- gallery-wrap .end// -->
                </aside>
                <aside class="col-sm-7">
                  <article class="card-body p-5">
                    <h3 class="title mb-3">{{ item.goods_name }}</h3>

                    <p class="price-detail-wrap">
                      <span class="price h3 text-warning">
                        <span class="num">{{ number_format(item.price) }}</span>
                      </span>
                      <span>원</span>
                    </p> <!-- price-detail-wrap .// -->

                    <dl class="item-property">
                      <dt>Description</dt>
                      <dd><p>{{ item.goods_description }}</p></dd>
                    </dl>
                    <!-- item-property-hor .// -->
                    <hr>

                    <div class="row">
                      <div class="col-sm-5">
                        <dl class="param param-inline">
                          <dt>Quantity: </dt>
                          <dd>
                            <input class="form-control" type="number" min="1" :max="item.goods_cnt"  name="quantity" v-model="quantity">
                          </dd>
                        </dl>  <!-- item-property .// -->
                      </div> <!-- col.// -->
                    </div> <!-- row.// -->

                    <hr>

                    <a href="#" @click="basket_add" class="btn btn-outline-primary text-uppercase"> <font-awesome-icon icon="fa-solid fa-shopping-cart" /> 장바구니에 담기 </a>
                  </article> <!-- card-body.// -->
                </aside> <!-- col.// -->
              </div> <!-- row.// -->
            </div> <!-- card.// -->
          </form>
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>
.gallery-wrap .img-big-wrap img {
    height: 450px;
    width: auto;
    display: inline-block;
    cursor: zoom-in;
}


.gallery-wrap .img-small-wrap .item-gallery {
    width: 60px;
    height: 60px;
    border: 1px solid #ddd;
    margin: 7px 2px;
    display: inline-block;
    overflow: hidden;
}

.gallery-wrap .img-small-wrap {
    text-align: center;
}
.gallery-wrap .img-small-wrap img {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
    border-radius: 4px;
    cursor: zoom-in;
}
</style>