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
      <li class="page-item" v-if="paginates.current > 1">
        <a class="page-link" href="#" @click="pageClick(1)">First</a>
      </li>
      <li class="page-item" v-if="paginates.prev !== null">
        <a class="page-link" href="#" @click="pageClick(paginates.prev)">Previous</a>
      </li>
      <li class="page-item" :class="{active: paginates.current === item}" :key="index" v-for="(item, index) in paginates.items">
        <a class="page-link" href="#" @click="pageClick(item)">{{ item }}</a>
      </li>
      <li class="page-item" v-if="paginates.next !== null">
        <a class="page-link" href="#" @click="pageClick(paginates.next)">Next</a>
      </li>
      <li class="page-item" v-if="paginates.current < this.total">
        <a class="page-link" href="#" @click="pageClick(this.total)">Last</a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>

</style>