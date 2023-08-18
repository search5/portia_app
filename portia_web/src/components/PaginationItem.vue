<script>
import {isPositiveInteger, paginate} from "../lib";

export default {
  name: "PaginationItem",
  props: {
    page: Number,
    total: Number
  },
  emits: ['page_click'],
  methods: {
    pageClick (page_no) {
      if (!isPositiveInteger(page_no)) return false
      this.$emit('page_click', page_no)
    }
  },
  computed: {
    paginates () {
      return paginate({current: this.page, max: this.total})
    }
  }
}
</script>

<template>
  <nav aria-label="Page navigation example">
    <ul class="pagination justify-content-center">
      <li class="page-item"><a class="page-link" href="#">First</a></li>
      <li class="page-item"><a class="page-link" href="#">Previous</a></li>
      <li class="page-item" :key="index" v-for="(item, index) in paginates.items">
        <a class="page-link" href="#" @click="pageClick(item)">{{ item }}</a>
      </li>
<!--      <li class="page-item"><a class="page-link" href="#">2</a></li>-->
<!--      <li class="page-item"><a class="page-link" href="#">3</a></li>-->
      <li class="page-item"><a class="page-link" href="#">Next</a></li>
      <li class="page-item"><a class="page-link" href="#">Last</a></li>
    </ul>
  </nav>
</template>

<style scoped>

</style>