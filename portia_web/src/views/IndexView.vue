<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";

import { Carousel } from 'bootstrap';
import {range} from "lodash-es";
import {mapActions} from "pinia";
import {useUsersStore} from "../stores/users";
import GoodsListItem from "../components/GoodsListItem.vue";

export default defineComponent({
  name: "IndexView",
  components: {GoodsListItem, FooterView, TopMenuView},
  data: () => ({
    carousel_images: [
      {src: '/api/placeholder/800x400', alt: '1'},
      {src: '/api/placeholder/800x400', alt: '2'},
      {src: '/api/placeholder/800x400', alt: '3'}
    ],
    input_data: {
      username: '',
      password: ''
    }
  }),
  methods: {
    range (value) {
      return range(value)
    },
    ...mapActions(useUsersStore, ['login_action']),
    login () {
      this.login_action(this.input_data).then(result => {
        if (result.success) {
          if (this.$router.currentRoute.value.name !== 'index') {
            this.$router.push({name: 'index'})
          } else {
            this.$router.go(0)
          }
        }
      }).catch(error => {
        alert('로그인에 실패했습니다')
      })
    }
  },
  computed: {
    ...mapActions(useUsersStore, ['is_login']),
    username () {
      return localStorage.getItem('username')
    }
  },
  mounted() {
    // const carousel = new Carousel('#carouselExampleControls')
    // console.log(carousel)

    // TODO
    // 상품 목록 가져오기
  }
})
</script>

<template>

  <div>
    <TopMenuView></TopMenuView>

    <!-- Page Content -->
    <div class="container">
      <div class="row">
        <div class="col-lg-3">
          <h1 class="my-4">Portia 쇼핑몰</h1>
          <div v-if="!is_login">
            <div class="row">
              <label for="inputEmail3" class="col-sm-4 col-form-label">이메일</label>
              <div class="col-sm-8">
                <input type="email" class="form-control form-control-sm" id="inputEmail3" v-model="input_data.username">
              </div>
            </div>
            <div class="row">
              <label for="inputPassword3" class="col-sm-4 col-form-label">비밀번호</label>
              <div class="col-sm-8">
                <input type="password" class="form-control form-control-sm" id="inputPassword3" v-model="input_data.password">
              </div>
            </div>
            <div class="row">
              <div class="col-sm-10 text-right">
                <button type="button" class="btn btn-success" @click="login">로그인</button>
              </div>
            </div>
          </div>
          <div v-if="is_login">
            {{ username }}님 로그인하셨습니다
          </div>
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

          <GoodsListItem limit="6"></GoodsListItem>
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