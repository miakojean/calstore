<template>
  <div class="main--container">
    <navbar @opencart="showCartModal = true"/>
    <aboutSection />
    <footerSection/>
    <cartmodal :isOpen="showCartModal" @close="showCartModal = false"/>
    <cookiesToast/>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import navbar from '../components/nav/navbar.vue';
import cartmodal from '../components/modal/cartmodal.vue';
import footerSection from '../components/section/footerSection.vue';
import cookiesToast from '../components/tools/cookiesToast.vue';
import aboutSection from '../components/section/aboutSection.vue';

const showCartModal = ref(false)
</script>

<style scoped>

</style>
