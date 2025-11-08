<template>
  <section>
    <h4>{{ title }}</h4>
    <p>Découvrir notre panoplie de chaussures</p>
    <div class="category__container" ref="scrollContainer" @scroll="handleScroll">
      <productcard 
        v-for="(card, index) in cards" 
        :key="index" 
        :product="getProductData(index)"
        @add-to-cart="addToCart"
      />
    </div>
    
    <!-- Indicateurs -->
    <div class="carousel-indicators">
      <span 
        v-for="(card, index) in cards" 
        :key="index"
        :class="['indicator', { active: currentIndex === index }]"
        @click="scrollToIndex(index)"
      ></span>
    </div>

    <morebutton label="Voir tous les articles"/>
  </section>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import productcard from '../card/productcard.vue'
import morebutton from '../button/morebutton.vue';
import { useCartStore } from '@/stores/cartStore'

export default {
  name: 'CategorySection',
  components: {
    productcard,
    morebutton
  },
  props: {
    title: {
      type: String,
      default: "Chaussures"
    }
  },
  setup(props) {
    const scrollContainer = ref<HTMLElement | null>(null)
    const currentIndex = ref(0)
    const cards = Array(5).fill(null)
    const cartStore = useCartStore()

    // Données des produits avec différentes images
    const products = [
      {
        id: 1,
        name: "Basket simple blanche",
        price: 89.99,
        image: "Copilot_20251107_112529.png", // Juste le nom du fichier
        description: "Basket blanche élégante et confortable",
        originalPrice: 129.99,
        discount: "-30%",
        rating: 4.5,
        reviewCount: 128
      },
      {
        id: 2,
        name: "Basket running noire", 
        price: 119.99,
        image: "Copilot_20251107_112743.png", // Juste le nom du fichier
        description: "Parfaite pour le sport",
        rating: 4.2,
        reviewCount: 89
      },
      {
        id: 3,
        name: "Soulier noir", 
        price: 119.99,
        image: "Copilot_20251107_112754.png", // Juste le nom du fichier
        description: "Parfaite pour cérémonie",
        rating: 4.2,
        reviewCount: 89
      },
      // ... autres produits
    ]

    const getProductData = (index: number) => {
      return products[index] || products[0]
    }

    const addToCart = (product: any) => {
      cartStore.addToCart({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image
      })
    }

    const setupCarousel = () => {
      if (scrollContainer.value) {
        scrollContainer.value.scrollLeft = 0
      }
    }

    const handleScroll = () => {
      if (scrollContainer.value) {
        const scrollLeft = scrollContainer.value.scrollLeft
        const cardWidth = scrollContainer.value.offsetWidth
        currentIndex.value = Math.round(scrollLeft / cardWidth)
      }
    }

    const scrollToIndex = (index: number) => {
      if (scrollContainer.value) {
        const cardWidth = scrollContainer.value.offsetWidth
        scrollContainer.value.scrollTo({
          left: index * cardWidth,
          behavior: 'smooth'
        })
      }
    }

    onMounted(() => {
      setupCarousel()
    })

    return {
      scrollContainer,
      currentIndex,
      cards,
      handleScroll,
      scrollToIndex,
      getProductData,
      addToCart
    }
  }
}
</script>

<style scoped>
.category__container {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  overflow-y: hidden;
  width: 100%;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  padding: 1rem 0;
}

.category__container::-webkit-scrollbar {
  display: none;
}

.category__container > * {
  flex: 0 0 auto;
  width: 100%;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}

/* Indicateurs */
.carousel-indicators {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.indicator.active {
  background-color: #000;
}

/* Debug panel */
.cart-debug {
  margin-top: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 0.5rem;
  border: 1px solid #ddd;
}

.cart-debug h5 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.debug-item {
  padding: 0.25rem 0;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
}

/* Animation d'ajout au panier */
.added-to-cart {
  animation: addToCart 1s ease;
}

@keyframes addToCart {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
</style>