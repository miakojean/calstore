<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
import navbar from '@/components/nav/navbar.vue';
import categorybar from '@/components/nav/categorybar.vue';
import categorysection from '@/components/section/categorysection.vue';
</script>

<template>
  <main>
    <navbar/>
    <TheWelcome />
    <categorybar/>
    <categorysection/>
    <categorysection title="Perruques"/>
    <categorysection title="T-shirt"/>
  </main>
</template>
