<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "TopMenuView"
})
</script>

<template>
  <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
    <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
      <img src="@/assets/logo.png" class="img-fluid" style="height: 40px;">
      <span class="fs-4">Portia Shop</span>
    </a>

    <ul class="nav nav-pills">
      <li class="nav-item"><a href="#" class="nav-link active" aria-current="page">처음 화면</a></li>
      <li class="nav-item">
        <RouterLink :to="{name: 'goods_list'}" class="nav-link">상품 목록</RouterLink>
      </li>
      <li class="nav-item"><a href="#" class="nav-link">회원 가입</a></li>
      <li class="nav-item"><a href="#" class="nav-link">로그인</a></li>
      <li class="nav-item"><a href="#" class="nav-link">장바구니</a></li>
    </ul>
  </header>
</template>

<style lang="scss" scoped>

</style>