<template>
  <div class="main--container">
    <navbar @opencart="showCartModal = true"/>
    <promotionsection/>
    <footerSection/>
    <cartmodal :isOpen="showCartModal" @close="showCartModal = false"/>
  </div>
</template>

<script>
import { ref } from 'vue';
import TheWelcome from '../components/TheWelcome.vue'
import navbar from '@/components/nav/navbar.vue';
import categorysection from '@/components/section/categorysection.vue';
import promotionsection from '@/components/section/promotionsection.vue';
import cartmodal from '@/components/modal/cartmodal.vue';
import footerSection from '@/components/section/footerSection.vue';

export default {
  name: 'HomePage',
  components: {
    TheWelcome,
    navbar,
    categorysection,
    promotionsection,
    cartmodal,
    footerSection
  },
  setup() {
    const showCartModal = ref(false)

    const handBag = ref([
      {
        id: 1,
        name: "Sac à main noir",
        price: 89.99,
        image: "Copilot_20251109_224858.png",
        description: "Basket blanche élégante et confortable",
        originalPrice: 129.99,
        discount: "-30%",
        rating: 4.5,
        reviewCount: 128
      },
      {
        id: 2,
        name: "Sac à main noir", 
        price: 119.99,
        image: "Copilot_20251109_225048.png",
        description: "Parfaite pour le sport",
        rating: 4.2,
        reviewCount: 89
      },
      {
        id: 3,
        name: "Soulier noir", 
        price: 119.99,
        image: "sac_a_main.png",
        description: "Parfaite pour cérémonie",
        rating: 4.2,
        reviewCount: 89
      }
    ])

    return {
      showCartModal,
      handBag
    }
  }
}
</script>