<script>
import {defineComponent} from 'vue'
import FooterView from "../components/FooterView.vue";
import TopMenuView from "../components/TopMenuView.vue";
import {range} from "lodash-es";
import {number_format} from "../lib";

export default defineComponent({
  name: "GoodsDetailView",
  components: {FooterView, TopMenuView},
  data: () => ({
    item: {
      id: 1,
      big_image: '/api/placeholder/525x450',
      thumbnails: [
        {small: '/api/placeholder/60x60', big: '/api/placeholder/700x400'},
        {small: '/api/placeholder/60x60', big: '/api/placeholder/700x400'},
        {small: '/api/placeholder/60x60', big: '/api/placeholder/700x400'},
        {small: '/api/placeholder/60x60', big: '/api/placeholder/700x400'},
        {small: '/api/placeholder/60x60', big: '/api/placeholder/700x400'}
      ],
      goods_name: '상품 1',
      price: 30000,
      goods_description: '올바른 상품입니다',
      goods_ranking: 3
    }
  }),
  methods: {
    number_format,
    range,
    basket_add () {
      // var form = document.querySelector("form")
      // form.action = "/basket/add";
      // form.submit();
      // TODO
    }
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
            <input type="hidden" name="goods_id" value="{ item.id }}">
            <div class="card mb-4">
              <div class="row">
                <aside class="col-sm-5 border-right">
                  <article class="gallery-wrap">
                    <div class="img-big-wrap">
                      <div>
                        <a href="#"><img :src="item.big_image"></a>
                      </div>
                    </div> <!-- slider-product.// -->
                    <div class="img-small-wrap">
                      <div class="item-gallery" :key="index" v-for="(entry, index) in item.thumbnails"><img :src="entry.small"></div>
                    </div> <!-- slider-nav.// -->
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

                    <span class="text-muted" :key="index" v-for="(val, index) in range(item.goods_ranking)">
                      &#9733;
                    </span>

                    <span class="text-muted" :key="index" v-for="(val, index) in range(5- item.goods_ranking)">
                      &#9734;
                    </span>
                    <!-- item-property-hor .// -->
                    <hr>

                    <div class="row">
                      <div class="col-sm-5">
                        <dl class="param param-inline">
                          <dt>Quantity: </dt>
                          <dd>
                            <select class="form-select" style="width:70px;" name="quantity">
                              <option>1</option>
                              <option>2</option>
                              <option>3</option>
                            </select>
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