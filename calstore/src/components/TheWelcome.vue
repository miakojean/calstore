<template>
  <section>
    <h2>Préparez vos fêtes avec calstore, profitez des promotions de fin d'année.</h2>
    <div class="btn__section">
      <mainbutton/>
      <seconbutton/>
    </div>
  </section>
</template>

<script lang="ts">
import mainbutton from './button/mainbutton.vue';
import seconbutton from './button/seconbutton.vue';
export default {
  components:{
    mainbutton,
    seconbutton
  }
}
</script>

<style scoped>
/* mobile */
section{
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.btn__section{
  width: 100%;
  display: flex;
  gap: 0.5rem;
}
</style>