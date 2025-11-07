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
import { ref, onMounted, computed } from 'vue'
import productcard from '../card/productcard.vue'
import seconbutton from '../button/seconbutton.vue';
import morebutton from '../button/morebutton.vue';
import { useCartStore } from '@/stores/cartStore'

// Interface pour les produits
interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  description: string;
}

export default {
  name: 'CategorySection',
  components: {
    productcard,
    seconbutton,
    morebutton
  },
  props: {
    title: {
      type: String,
      default: "Chaussures"
    }
  },
  setup(props) {
    // Refs
    const scrollContainer = ref<HTMLElement | null>(null)
    const currentIndex = ref(0)
    const cards = Array(5).fill(null)
    const showDebug = ref(true) // Mettre à false pour cacher le debug

    // Store Panier
    const cartStore = useCartStore()

    // Données des produits (simulées)
    const products: Product[] = [
      {
        id: 1,
        name: "Basket simple blanche",
        price: 89.99,
        image: "../../assets/pic/Copilot_20251107_112529.png",
        description: "Basket blanche élégante et confortable"
      },
      {
        id: 2,
        name: "Basket running noire",
        price: 119.99,
        image: "../../assets/pic/sneaker-black.jpg",
        description: "Parfaite pour le sport"
      },
      {
        id: 3,
        name: "Chaussure ville marron",
        price: 149.99,
        image: "../../assets/pic/shoes-brown.jpg",
        description: "Style classique et raffiné"
      },
      {
        id: 4,
        name: "Basket colorée",
        price: 79.99,
        image: "../../assets/pic/sneaker-color.jpg",
        description: "Pour un look décontracté"
      },
      {
        id: 5,
        name: "Chaussure de luxe",
        price: 199.99,
        image: "../../assets/pic/luxury-shoes.jpg",
        description: "Élégance et sophistication"
      }
    ]

    // Computed du store
    const cart = computed(() => cartStore.cart)
    const totalItems = computed(() => cartStore.totalItems)
    const totalPrice = computed(() => cartStore.totalPrice)

    // Méthodes
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

    // Obtenir les données du produit par index
    const getProductData = (index: number): Product => {
      return products[index] || products[0]
    }

    // Ajouter au panier
    const addToCart = (product: Product) => {
      console.log('Ajout au panier:', product)
      cartStore.addToCart({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image
      })
      
      // Feedback visuel
      const addedProduct = document.querySelector(`[data-product-id="${product.id}"]`)
      if (addedProduct) {
        addedProduct.classList.add('added-to-cart')
        setTimeout(() => {
          addedProduct.classList.remove('added-to-cart')
        }, 1000)
      }
    }

    // Lifecycle
    onMounted(() => {
      setupCarousel()
      console.log('Store panier chargé:', cartStore.cart)
    })

    // Return everything that should be available in template
    return {
      scrollContainer,
      currentIndex,
      cards,
      cart,
      totalItems,
      totalPrice,
      showDebug,
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