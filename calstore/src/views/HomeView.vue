<script lang="ts">
import { defineComponent, ref } from 'vue'
import TheWelcome from '../components/TheWelcome.vue'
import navbar from '@/components/nav/navbar.vue';
import categorysection from '@/components/section/categorysection.vue';
import newslettersection from '@/components/section/newslettersection.vue';
import cartmodal from '@/components/modal/cartmodal.vue';

export default defineComponent({
  name: 'HomePage',
  components: {
    TheWelcome,
    navbar,
    categorysection,
    newslettersection,
    cartmodal
  },
  setup() {
    const showCartModal = ref(false)

    return {
      showCartModal
    }
  }
})
</script>

<template>
  <main>
    <navbar @opencart="showCartModal = true"/>
    <TheWelcome />
    <h3>Catégories de produits</h3>
    <categorysection />
    <categorysection title="Perruques"/>
    <categorysection title="T-shirt"/>
    <h3>Restez au courant des nouveautés</h3>
    <newslettersection />
    <cartmodal :isOpen="showCartModal" @close="showCartModal = false"/>
  </main>
</template>