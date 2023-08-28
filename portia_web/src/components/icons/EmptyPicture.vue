<script>
import {split} from "lodash-es";

export default {
  name: "EmptyPicture",
  props: {
    size: String
  },
  computed: {
    bg_fill () {
      return '#ccc'
    },
    txt_fill () {
      return '#9c9c9c'
    },
    txt () {
      return this.size
    },
    width () {
      return split(this.size, 'x')[0]
    },
    height () {
      return split(this.size, 'x')[1]
    }
  }
}
</script>

<template>
  <svg class="bd-placeholder-img me-2" :width="width" :height="height" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice" focusable="false">
    <rect width="100%" height="100%" :fill="bg_fill"/>
    <text x="40%" y="50%" :fill="txt_fill" dy=".3em" v-if="txt !== null" font-size="2.7em">{{ txt }}</text>
  </svg>
</template>
