<script>
import {defineComponent} from 'vue'
import {useUsersStore} from "../stores/users";
import {mapActions, mapState} from "pinia";

export default defineComponent({
  name: "TopMenuView",
  methods: {
    portia_logout () {
      const access_token = localStorage.getItem('access_token')
      const refresh_token = localStorage.getItem('refresh_token')

      if (access_token !== null && refresh_token !== null) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('username')
      }

      if (this.$router.currentRoute.value.name !== 'index') {
        this.$router.push({name: 'portia_login'})
      } else {
        this.$router.go(0)
      }
    },
    location_active(dest_location) {
      return location.pathname === dest_location
    }
  },
  computed: {
    ...mapActions(useUsersStore, ['is_login', 'is_admin']),
    username () {
      return localStorage.getItem('username')
    }
  }
})
</script>

<template>
  <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
    <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
      <img src="@/assets/logo.png" class="img-fluid" style="height: 40px;">
      <span class="fs-4">Portia Shop</span>
    </a>

    <ul class="nav nav-pills">
      <li class="nav-item">
        <a href="/" class="nav-link" :class="{active: location_active('/') }">처음 화면</a>
      </li>
      <li class="nav-item">
        <RouterLink :to="{name: 'goods_list'}" class="nav-link" :class="{active: location_active('/goods') }">상품 목록</RouterLink>
      </li>
      <li class="nav-item" v-if="!is_login">
        <RouterLink :to="{name: 'portia_join'}" class="nav-link" :class="{active: location_active('/join_member') }">회원 가입</RouterLink>
      </li>
      <li class="nav-item" v-if="!is_login">
        <RouterLink :to="{name: 'portia_login'}" class="nav-link" :class="{active: location_active('/login') }">로그인</RouterLink>
      </li>
      <li class="nav-item" v-if="is_login">
        <RouterLink :to="{name: 'mypage'}" class="nav-link" :class="{active: location_active('/mypage') }">마이페이지</RouterLink>
      </li>
      <li class="nav-item" v-if="is_login">
        <RouterLink :to="{name: 'basket_list'}" class="nav-link" :class="{active: location_active('/basket') }">장바구니</RouterLink>
      </li>
      <li class="nav-item" v-if="is_admin">
        <RouterLink :to="{name: 'admin_goods_list', query: {page: 1}}" class="nav-link" :class="{active: location_active('/admin/goods') }">관리자</RouterLink>
      </li>
      <li class="nav-item" v-if="is_login">
        <a href="#" @click="portia_logout" class="nav-link">{{ username }}님 로그아웃</a>
      </li>
    </ul>
  </header>
</template>

<style lang="scss" scoped>

</style>