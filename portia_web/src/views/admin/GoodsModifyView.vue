<script>
import TopMenuView from "../../components/TopMenuView.vue";
import AdminLeftView from "../../components/AdminLeftView.vue";
import FooterView from "../../components/FooterView.vue";

export default {
  name: "GoodsModifyView",
  components: {FooterView, AdminLeftView, TopMenuView}
}
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="d-flex flex-row flex-shrink-0 p-3 bg-body-tertiary">
      <AdminLeftView></AdminLeftView>

      <div class="container">
        <div class="mb-3">
          <label for="exampleFormControlInput1" class="form-label">상품 코드</label>
          <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
        </div>
        <div class="mb-3">
          <label for="exampleFormControlTextarea1" class="form-label">상품명</label>
          <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
        </div>
        <div class="mb-3">
          <label for="exampleFormControlTextarea1" class="form-label">가격</label>
          <input type="number" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
        </div>
        <div class="mb-3">
          <label for="exampleFormControlTextarea1" class="form-label">사진</label>
          <input type="file" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
        </div>
        <div class="mb-3">
          <label for="exampleFormControlTextarea1" class="form-label">재고</label>
          <input type="number" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
        </div>
        <div class="mb-3">
          <label for="exampleFormControlTextarea1" class="form-label">설명</label>
          <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
        </div>

        <button class="btn btn-primary">수정하기</button>
        <button class="btn btn-warning">취소하기</button>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>