<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";

export default defineComponent({
  name: "MyOrdersView",
  components: {TopMenuView, FooterView}
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>