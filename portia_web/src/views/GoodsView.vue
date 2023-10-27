<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";
import {range} from "lodash-es";
import {number_format} from "../lib";

export default defineComponent({
  name: "GoodsView",
  components: {FooterView, TopMenuView},
  data: () => ({
    goods: [
      {
        id: 1,
        thumbnail: '/api/placeholder/700x400',
        goods_name: '상품 1',
        price: 30000,
        goods_description: '올바른 상품입니다'
      }, {
        id: 2,
        thumbnail: '/api/placeholder/700x400',
        goods_name: '상품 2',
        price: 28000,
        goods_description: '잘나가는 책입니다'
      }
    ]
  }),
  methods: {
    number_format,
    range (value) {
      return range(value)
    }
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container mt-4">
      <div class="row">
        <div class="col-12">
          <div class="row">
            <div class="col-lg-4 col-md-6 mb-4" :key="index" v-for="(item, index) in goods">
              <div class="card h-100">
                <a href="#"><img class="card-img-top" :src="item.thumbnail" alt=""></a>
                <div class="card-body">
                  <h4 class="card-title">
                    <a :href="'/goods/' + item.id">{{ item.goods_name }} </a>
                  </h4>
                  <h5>{{ number_format(item.price) }}</h5>
                  <p class="card-text">{{ item.goods_description }}</p>
                </div>
                <div class="card-footer"></div>
              </div>
            </div>
          </div>
          <!-- /.row -->
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>