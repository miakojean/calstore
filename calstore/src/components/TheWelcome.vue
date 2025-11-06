<template>
  <section>
    <h1>Bienvenu au pays mon fils !!!</h1>
  </section>
</template>

<script>
import categorybar from './nav/categorybar.vue';
export default {
  components:{
    categorybar
  }
}
</script>

<style scoped>
section{
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>