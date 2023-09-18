<script>
import PaginationItem from "../../components/PaginationItem.vue";

export default {
  name: "GoodsListView",
  components: {PaginationItem}
}
</script>

<template>
  <div class="container mt-3">
    <h3>상품 목록</h3>
    <table class="table table-bordered table-hover">
      <thead>
      <tr>
        <th>상품 코드</th>
        <th>상품명</th>
        <th>가격</th>
        <th>재고</th>
        <th>등록일</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
      </tr>
      </tbody>
    </table>

    <PaginationItem :page="1" :total="30"></PaginationItem>

    <RouterLink :to="{name: 'admin_goods_register'}" class="btn btn-primary">상품 추가</RouterLink>
  </div>
</template>

<style scoped>

</style>