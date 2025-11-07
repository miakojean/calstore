<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
import navbar from '@/components/nav/navbar.vue';
import categorysection from '@/components/section/categorysection.vue';
import newslettersection from '@/components/section/newslettersection.vue';
</script>

<template>
  <main>
    <navbar/>
    <TheWelcome />
    <h3>Catégories de produits</h3>
    <categorysection/>
    <categorysection title="Perruques"/>
    <categorysection title="T-shirt"/>
    <h3>Restez aux courants des nouveautés</h3>
    <newslettersection/>
  </main>
</template>
