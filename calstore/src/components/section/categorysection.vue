<template>
  <section class="category-section">
    <div class="section-header">
      <h4 class="section-title">{{ title }}</h4>
      <p class="section-description">{{ description }}</p>
    </div>
    
    <!-- État de chargement -->
    <div v-if="categoryStore.loadingStates[slug]" class="category__container">
      <ProductCardSkeleton v-for="n in 4" :key="`skeleton-${n}`"/>
    </div>
    
    <!-- État normal -->
    <div v-else class="category__container" ref="scrollContainer" @scroll="handleScroll">
      <productcard 
        v-for="(product, index) in products" 
        :key="product.id || `product-${index}`" 
        :product="product"
        @add-to-cart="addToCart"
        @show-product-detail="showProductDetail"
      />
    </div>
    
    <!-- Indicateurs seulement si chargement terminé et produits existent -->
    <div v-if="!categoryStore.loadingStates[slug] && products.length > 0" class="carousel-indicators">
      <span 
        v-for="(product, index) in products" 
        :key="product.id || `indicator-${index}`"
        :class="['indicator', { active: currentIndex === index }]"
        @click="scrollToIndex(index)"
      ></span>
    </div>

    <div class="section-footer">
      <morebutton :label="buttonLabel" @click="$emit('view-all')"/>
    </div>

    <ProductDetailModal 
      :isOpen="isOpen" 
      :product="selectedProduct" 
      @close="closeModal" 
      @add-to-cart="addToCart"
    />
  </section>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'

// Components
import productcard from '../card/productcard.vue'
import morebutton from '../button/morebutton.vue';
import ProductCardSkeleton from '../card/ProductCardSkeleton.vue';
import ProductDetailModal from '../modal/ProductDetailModal.vue';

// Store et Types
import { useCartStore } from '../../stores/cartStore'
import { useCategoryStore, type Product } from '../../stores/categoryStore';

export default {
  name: 'CategorySection',
  components: {
    productcard,
    morebutton,
    ProductDetailModal,
    ProductCardSkeleton
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
    buttonLabel: {
      type: String,
      default: "Voir tous les articles"
    },
    slug: {
      type: String,
      default: "chaussures"
    }
  },
  emits: ['view-all'],
  setup(props, { emit }) {
    const scrollContainer = ref<HTMLElement | null>(null)
    const currentIndex = ref(0);
    const cartStore = useCartStore();
    const categoryStore = useCategoryStore();
    let resizeObserver: ResizeObserver | null = null
    
    // État modal
    const isOpen = ref(false);
    const selectedProduct = ref<Product | null>(null);
    
    // CHANGEZ CECI : Utiliser les computed spécifiques à la catégorie
    const products = computed(() => {
      return categoryStore.getProductsBySlug(props.slug).value;
    });
    
    const isLoading = computed(() => {
      return categoryStore.isLoadingForSlug(props.slug).value;
    });

    const addToCart = (product: Product) => {
      cartStore.addToCart({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.main_image_url || ''
      })
    }

    const showProductDetail = (product: Product) => {
      selectedProduct.value = product;
      isOpen.value = true;
    };

    const closeModal = () => {
      isOpen.value = false;
      selectedProduct.value = null;
    };

    // --- LOGIQUE CARROUSEL ---
    
    const getStepWidth = (): number => {
      if (scrollContainer.value && scrollContainer.value.children.length > 0) {
        const firstCard = scrollContainer.value.children[0] as HTMLElement
        const cardStyle = window.getComputedStyle(firstCard)
        const containerStyle = window.getComputedStyle(scrollContainer.value)

        const cardWidth = firstCard.offsetWidth + parseFloat(cardStyle.marginLeft) + parseFloat(cardStyle.marginRight)
        const gap = parseFloat(containerStyle.gap) || 0 

        return cardWidth + gap
      }
      return 0
    }

    const setupCarousel = () => {
      if (scrollContainer.value) {
        scrollContainer.value.scrollLeft = 0
      }
      currentIndex.value = 0
    }

    const handleScroll = () => {
      if (scrollContainer.value) {
        const scrollLeft = scrollContainer.value.scrollLeft
        const stepWidth = getStepWidth()

        if (stepWidth > 0) {
          currentIndex.value = Math.round(scrollLeft / stepWidth)
        }
      }
    }

    const scrollToIndex = (index: number) => {
      if (scrollContainer.value) {
        const stepWidth = getStepWidth()
        scrollContainer.value.scrollTo({
          left: index * stepWidth,
          behavior: 'smooth'
        })
      }
    }

    const handleResize = () => {
      setupCarousel()
    }
    // --- FIN LOGIQUE CARROUSEL ---

    onMounted(async() => {
      // Initialiser le carrousel
      setTimeout(() => {
        setupCarousel()
      }, 100)
      
      // Observer les changements de taille
      if (scrollContainer.value) {
        resizeObserver = new ResizeObserver(handleResize)
        resizeObserver.observe(scrollContainer.value)
      }

      // Récupérer les produits de la catégorie seulement si nécessaire
      if (products.value.length === 0) {
        await categoryStore.fetchCategoryWithProducts(props.slug);
      }
    })

    onUnmounted(() => {
      if (resizeObserver) {
        resizeObserver.disconnect()
      }
    })

    return {
      categoryStore,
      scrollContainer,
      currentIndex,
      isOpen,
      selectedProduct,
      products,
      isLoading, // <-- Ajoutez ceci
      showProductDetail,
      closeModal,
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
  padding: 1rem;
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

  .indicator {
    width: 10px;
    height: 10px;
  }
}

/* Desktop - Pleine largeur */
@media (min-width: 1024px) {
  .category-section {
    width: 100%;
    max-width: none;
    margin: 0;
    padding: 3rem 2rem;
  }

  .category__container {
    width: 100%;
    gap: 2rem;
    padding: 0;
    overflow-x: visible;
    flex-wrap: wrap;
    justify-content: center;
  }

  .category__container > * {
    flex: 0 0 calc(25% - 1.5rem);
    scroll-snap-align: none;
  }

  .section-header {
    text-align: left;
    padding: 0;
    margin-bottom: 2rem;
  }

  .section-footer {
    padding: 2rem 0 0 0;
  }
  
  /* Cache la navigation mobile sur desktop */
  .carousel-indicators {
    display: none;
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