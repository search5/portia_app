<script>
import {defineComponent} from 'vue'
import TopMenuView from "@/components/TopMenuView.vue";
import FooterView from "@/components/FooterView.vue";

export default defineComponent({
  name: "MyPageView",
  components: {FooterView, TopMenuView}
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