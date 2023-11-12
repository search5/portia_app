<script>
import TopMenuView from "@/components/TopMenuView.vue";
import FooterView from "@/components/FooterView.vue";

export default {
  name: "OrdersView",
  components: {FooterView, TopMenuView}
}
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container mb-3">
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>