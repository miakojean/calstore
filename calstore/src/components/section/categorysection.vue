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
    
    <div class="carousel-indicators">
      <span 
        v-for="(product, index) in products" 
        :key="product.id || index"
        :class="['indicator', { active: currentIndex === index }]"
        @click="scrollToIndex(index, products.length)"
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
import { useCartStore } from '../../stores/cartStore'

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
        },
        {
          id: 3, // Attention: ID en double, vous devriez avoir un ID unique
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

    // --- LOGIQUE MISE À JOUR ---

    /**
     * Calcule la largeur de défilement pour un "pas" 
     * (largeur d'une carte + l'espace 'gap')
     */
    const getStepWidth = (): number => {
      if (scrollContainer.value && scrollContainer.value.children.length > 0) {
        // 1. Obtenir la première carte
        const firstCard = scrollContainer.value.children[0] as HTMLElement
        // 2. Obtenir son style calculé
        const cardStyle = window.getComputedStyle(firstCard)
        // 3. Obtenir le style du conteneur (pour le 'gap')
        const containerStyle = window.getComputedStyle(scrollContainer.value)

        // 4. Calculer la largeur totale de la carte (incluant marge, si besoin)
        const cardWidth = firstCard.offsetWidth + parseFloat(cardStyle.marginLeft) + parseFloat(cardStyle.marginRight)
        
        // 5. Obtenir l'espace 'gap'
        // Utilise parseFloat pour gérer les "rem" ou "px" et || 0 comme fallback
        const gap = parseFloat(containerStyle.gap) || 0 

        // Le "pas" est la largeur de la carte + l'espace
        return cardWidth + gap
      }
      return 0
    }

    /**
     * Réinitialise le scroll et l'index
     */
    const setupCarousel = () => {
      if (scrollContainer.value) {
        scrollContainer.value.scrollLeft = 0
      }
      currentIndex.value = 0 // Important : réinitialiser l'index
    }

    /**
     * Met à jour l'index en fonction de la position de défilement
     */
    const handleScroll = () => {
      if (scrollContainer.value) {
        const scrollLeft = scrollContainer.value.scrollLeft
        const stepWidth = getStepWidth()

        // S'assurer de ne pas diviser par zéro
        if (stepWidth > 0) {
          // Utiliser Math.round pour "snapper" à l'index le plus proche
          currentIndex.value = Math.round(scrollLeft / stepWidth)
        }
      }
    }

    /**
     * Fait défiler le carrousel vers un index spécifique
     */
    const scrollToIndex = (index: number, productLength: number) => {
      if (scrollContainer.value) {
        const stepWidth = getStepWidth()
        scrollContainer.value.scrollTo({
          left: index * stepWidth,
          behavior: 'smooth'
        })
      };
      console.log(`vous avez ${productLength - 1} élements à afficher`)
    }

    /**
     * Gère le redimensionnement de la fenêtre
     */
    const handleResize = () => {
      // Réinitialise le carrousel pour recalculer les positions
      setupCarousel()
    }

    // --- FIN DE LA LOGIQUE MISE À JOUR ---

    onMounted(() => {
      // Attendre un tick que le DOM soit prêt, surtout pour getStepWidth
      setTimeout(() => {
        setupCarousel()
      }, 0)
      
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
    width: 100%;
    gap: 1.5rem;
    padding: 1.5rem 1rem;
  }

  .category__container > * {
    flex: 0 0 calc(50% - 0.75rem);
  }

  /* AMÉLIORATION : S'assurer qu'ils restent cachés 
  .carousel-indicators {
    display: none;
  } */

  .indicator {
    width: 10px;
    height: 10px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .category-section {
    padding: 3rem 1rem;
  }

  .category__container {
    width: 100%;
    gap: 2rem;
    padding: 2rem 1rem;
    background:  #f0f4f8;;
    border-radius: 0.5rem;
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
  
  /* AMÉLIORATION : S'assurer qu'ils restent cachés 
  .carousel-indicators {
    display: none;
  } */
}

/* Large Desktop */
@media (min-width: 1280px) {

  .category__container {
    width: 100%;
    gap: 2rem;
    padding: 2rem;
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