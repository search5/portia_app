<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";
import {range} from "lodash-es";
import GoodsListItem from "../components/GoodsListItem.vue";

export default defineComponent({
  name: "GoodsView",
  components: {GoodsListItem, FooterView, TopMenuView},
  data: () => ({
  }),
  methods: {
    range (value) {
      return range(value)
    }
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container mt-4">
      <div class="row">
        <div class="col-12">
          <GoodsListItem></GoodsListItem>
          <!-- /.row -->
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>