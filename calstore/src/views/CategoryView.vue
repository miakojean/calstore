<template>
  <div class="main--container">
    <navbar @opencart="showCartModal = true" />
    <categorysection 
      :title="currentCategory"
      :slug="currentCategory" 

    />
    <footerSection/>
    <cartmodal :isOpen="showCartModal" @close="showCartModal = false"/>
  </div>
</template>

<script>
import { computed, onMounted, ref, watch } from 'vue';
import TheWelcome from '../components/TheWelcome.vue'
import navbar from '@/components/nav/navbar.vue';
import categorysection from '@/components/section/categorysection.vue';
import cartmodal from '@/components/modal/cartmodal.vue';
import footerSection from '@/components/section/footerSection.vue';
import { useRoute } from 'vue-router';
import { useCategoryStore } from '@/stores/categoryStore';

export default {
  name: 'HomePage',
  components: {
    TheWelcome,
    navbar,
    categorysection,
    cartmodal,
    footerSection
  },
  setup() {

    // state
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
    ]);

    const categoryStore = useCategoryStore();
    const route = useRoute()

    // Au lieu de route.name
    const currentCategory = computed(() => route.params.slug);

    // getters

    // actions

    onMounted(()=>{
      console.log('Vous êtes actuellement dans', currentCategory.value)
    })

    watch(currentCategory, ()=>{
      console.log('Nouvelle route détectée', currentCategory.value)
    })

    return {
      //state
      showCartModal,
      handBag,
      categoryStore,
      route,
      currentCategory

      //getter
    }
  }
}
</script>