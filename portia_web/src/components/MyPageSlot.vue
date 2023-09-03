<script>
export default {
  name: "MyPageSlot"
}
</script>

<template>
<div class="container">
      <div class="row">
        <div class="col-2">
          <ul class="list-group list-group-flush">
            <RouterLink class="list-group-item list-group-item-action" :to="{ name: 'myinfo' }">내 정보</RouterLink>
            <RouterLink class="list-group-item list-group-item-action" :to="{ name: 'myorder', query: {page: 1} }">구매 내역</RouterLink>
          </ul>
        </div>
        <div class="col-10">
          <slot></slot>
        </div>
      </div>
    </div>
</template>

<style scoped>

</style>