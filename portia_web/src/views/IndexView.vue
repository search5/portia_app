<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";

import { Carousel } from 'bootstrap';
import {range} from "lodash-es";
import {number_format} from "../lib";

export default defineComponent({
  name: "IndexView",
  components: {FooterView, TopMenuView},
  data: () => ({
    carousel_images: [
      {src: '/api/placeholder/800x400', alt: '1'},
      {src: '/api/placeholder/800x400', alt: '2'},
      {src: '/api/placeholder/800x400', alt: '3'}
    ],
    goods: [
      {
        id: 1,
        thumbnail: '/api/placeholder/700x400',
        goods_name: '상품 1',
        price: 30000,
        goods_description: '올바른 상품입니다',
        goods_ranking: 3
      }, {
        id: 2,
        thumbnail: '/api/placeholder/700x400',
        goods_name: '상품 2',
        price: 28000,
        goods_description: '잘나가는 책입니다',
        goods_ranking: 4
      }
    ]
  }),
  methods: {
    number_format,
    range (value) {
      return range(value)
    }
  },
  mounted() {
    // const carousel = new Carousel('#carouselExampleControls')
    // console.log(carousel)
  }
})
</script>

<template>

  <div>
    <TopMenuView></TopMenuView>

    <!-- Page Content -->
    <div class="container">
  <!--    {% with messages = get_flashed_messages() %}-->
  <!--      {% if messages %}-->
  <!--      <div class="alert alert-danger mt-3" role="alert"></div>-->
  <!--        <ul class=flashes>-->
  <!--        {% for message in messages %}-->
  <!--          <li>{{ message }}</li>-->
  <!--        {% endfor %}-->
  <!--        </ul>-->
  <!--      </div>-->
  <!--      {% endif %}-->
  <!--    {% endwith %}-->

      <div class="row">
        <div class="col-lg-3">
          <h1 class="my-4">Portia 쇼핑몰</h1>
  <!--        {% if not session.email %}-->
          <form method="post" action="/login">
              <div class="form-group row">
                <label for="inputEmail3" class="col-sm-4 col-form-label">이메일</label>
                <div class="col-sm-8">
                  <input type="email" class="form-control form-control-sm" id="inputEmail3" name="email">
                </div>
              </div>
              <div class="form-group row">
                <label for="inputPassword3" class="col-sm-4 col-form-label">비밀번호</label>
                <div class="col-sm-8">
                  <input type="password" class="form-control form-control-sm" id="inputPassword3" name="password">
                </div>
              </div>
              <div class="form-group row">
                <div class="col-sm-10 text-right">
                  <button type="submit" class="btn btn-success">로그인</button>
                </div>
              </div>
            </form>
  <!--          {% else %}-->
  <!--            {{ session['email'] }}님 로그인하셨습니다.-->
  <!--          {% endif %}-->
        </div>
        <!-- /.col-lg-3 -->

        <div class="col-lg-9">
          <div id="carouselExampleIndicators" class="carousel slide mb-2" data-bs-ride="true">
            <div class="carousel-indicators">
              <button type="button" data-bs-target="#carouselExampleIndicators" :data-bs-slide-to="index" :class="{active: index === 0}" :aria-current="{active: index === 0 ? 'true' : ''}" :aria-label="'Slide ' + (index + 1)" v-for="(item, index) in carousel_images" :key="index"></button>
            </div>
            <div class="carousel-inner">
              <div class="carousel-item" :class="{active: index === 0}" v-for="(item, index) in carousel_images" :key="index">
                <img :src="item.src" class="d-block w-100" :alt="item.alt">
              </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">이전</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">다음</span>
            </button>
          </div>

          <div class="row">

            <div class="col-lg-4 col-md-6 mb-4" :key="index" v-for="(item, index) in goods">
              <div class="card h-100">
                <a href="#"><img class="card-img-top" :src="item.thumbnail" alt=""></a>
                <div class="card-body">
                  <h4 class="card-title">
                    <RouterLink :to="{name: 'goods_view', params: {id: item.id}}">{{ item.goods_name }}</RouterLink>
                  </h4>
                  <h5>{{ number_format(item.price) }}</h5>
                  <p class="card-text">{{ item.goods_description }}</p>
                </div>
                <div class="card-footer">
                  <small class="text-muted" :key="index" v-for="(val, index) in range(item.goods_ranking)">
                    &#9733;
                  </small>

                  <small class="text-muted" :key="index" v-for="(val, index) in range(5- item.goods_ranking)">
                    &#9734;
                  </small>
                </div>
              </div>
            </div>
          </div>
          <!-- /.row -->

        </div>
        <!-- /.col-lg-9 -->

      </div>
      <!-- /.row -->
    </div>
    <!-- /.container -->

    <FooterView></FooterView>
  </div>
</template>

<style lang="scss" scoped>

</style>