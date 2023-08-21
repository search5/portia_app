<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
<!--        <RouterLink to="/">Home</RouterLink>-->
<!--        <RouterLink to="/about">About</RouterLink>-->
  <RouterView />
</template>

<style lang="scss" scoped>
// Variable overrides first
//$primary: #900;
$enable-shadows: true;
$prefix: "mo-";

// Then import Bootstrap
@import "bootstrap/scss/bootstrap";
</style>