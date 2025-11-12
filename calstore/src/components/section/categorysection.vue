<template>
  <section class="category-section">
    <div class="section-header">
      <h4 class="section-title">{{ title }}</h4>
      <p class="section-description">{{ description }}</p>
    </div>
    
    <div class="category__container" ref="scrollContainer" @scroll="handleScroll">
      <productcard 
        v-for="(product, index) in products" 
        :key="product.id || index" 
        :product="product"
        @add-to-cart="addToCart"
      />
    </div>
    
    <!-- Indicateurs -->
    <div class="carousel-indicators">
      <span 
        v-for="(product, index) in products" 
        :key="product.id || index"
        :class="['indicator', { active: currentIndex === index }]"
        @click="scrollToIndex(index)"
      ></span>
    </div>

    <div class="section-footer">
      <morebutton :label="buttonLabel" @click="$emit('view-all')"/>
    </div>
  </section>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import productcard from '../card/productcard.vue'
import morebutton from '../button/morebutton.vue';
import { useCartStore } from '@/stores/cartStore'

// Interface pour les produits
interface Product {
  id: number | string;
  name: string;
  price: number;
  image: string;
  description?: string;
  originalPrice?: number;
  discount?: string;
  rating?: number;
  reviewCount?: number;
}

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
    },
    description: {
      type: String,
      default: "Découvrir notre panoplie de chaussures"
    },
    products: {
      type: Array as () => Product[],
      default: () => [
        {
          id: 1,
          name: "Basket simple blanche",
          price: 89.99,
          image: "Copilot_20251107_112529.png",
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
          image: "Copilot_20251107_112743.png",
          description: "Parfaite pour le sport",
          rating: 4.2,
          reviewCount: 89
        },
        {
          id: 3,
          name: "Soulier noir", 
          price: 119.99,
          image: "Copilot_20251107_112754.png",
          description: "Parfaite pour cérémonie",
          rating: 4.2,
          reviewCount: 89
        }
      ]
    },
    buttonLabel: {
      type: String,
      default: "Voir tous les articles"
    }
  },
  emits: ['view-all'],
  setup(props, { emit }) {
    const scrollContainer = ref<HTMLElement | null>(null)
    const currentIndex = ref(0)
    const cartStore = useCartStore()
    let resizeObserver: ResizeObserver | null = null

    const addToCart = (product: Product) => {
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

    const handleResize = () => {
      // Réinitialiser le scroll lors du redimensionnement
      setupCarousel()
    }

    onMounted(() => {
      setupCarousel()
      
      // Observer les changements de taille pour le responsive
      if (scrollContainer.value) {
        resizeObserver = new ResizeObserver(handleResize)
        resizeObserver.observe(scrollContainer.value)
      }
    })

    onUnmounted(() => {
      if (resizeObserver) {
        resizeObserver.disconnect()
      }
    })

    return {
      scrollContainer,
      currentIndex,
      handleScroll,
      scrollToIndex,
      addToCart
    }
  }
}
</script>

<style scoped>
.category-section {
  padding: 1rem 0.5rem;
  width: 100%;
}

.section-header {
  text-align: center;
  margin-bottom: 1.5rem;
  padding: 0 0.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.section-description {
  font-size: 0.9rem;
  color: #6b7280;
  line-height: 1.4;
}

.category__container {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  overflow-y: hidden;
  width: 100%;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  padding: 1rem 0.5rem;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.category__container::-webkit-scrollbar {
  display: none;
}

.category__container > * {
  flex: 0 0 85%;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}

/* Indicateurs */
.carousel-indicators {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin: 1.5rem 0;
  padding: 0 0.5rem;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #d1d5db;
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background-color: #000;
  transform: scale(1.2);
}

.section-footer {
  display: flex;
  justify-content: center;
  padding: 0 0.5rem;
}

/* Tablet */
@media (min-width: 768px) {
  .category-section {
    padding: 2rem 1rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .section-header {
    text-align: left;
    margin-bottom: 2rem;
    padding: 0 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .section-description {
    font-size: 1rem;
  }

  .category__container {
    gap: 1.5rem;
    padding: 1.5rem 1rem;
  }

  .category__container > * {
    flex: 0 0 calc(50% - 0.75rem);
  }

  .carousel-indicators {
    margin: 2rem 0;
  }

  .indicator {
    width: 10px;
    height: 10px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .category-section {
    padding: 3rem 2rem;
  }

  .category__container {
    gap: 2rem;
    padding: 2rem;
  }

  .category__container > * {
    flex: 0 0 calc(33.333% - 1.33rem);
  }

  .section-header {
    padding: 0 2rem;
  }

  .section-footer {
    padding: 0 2rem;
  }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .category__container > * {
    flex: 0 0 calc(25% - 1.5rem);
  }
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