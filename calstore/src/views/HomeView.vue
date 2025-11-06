<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
import navbar from '@/components/nav/navbar.vue';
import categorybar from '@/components/nav/categorybar.vue';
</script>

<template>
  <main>
    <navbar/>
    <categorybar/>
    <TheWelcome />
  </main>
</template>
