<template>
  <main>
    <navbar />
    <checkoutSection />
  </main>
</template>

<script>
import navbar from '@/components/nav/navbar.vue';
import checkoutSection from '@/components/section/checkoutSection.vue';
export default {
  components: {
    navbar,
    checkoutSection
  }
}
</script>

<style scoped>

</style>