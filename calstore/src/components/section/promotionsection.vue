<template>
  <section class="category-section">
    <div class="section-header">
      <h4 class="section-title">{{ title }}</h4>
      <p class="section-description">{{ description }}</p>
    </div>

    <!-- État de chargement : 1 skeleton mobile, 3 desktop -->
    <div v-if="promotionStore.loading" class="skeleton-container">
      <ProductCardSkeleton v-for="i in skeletonCount" :key="i" />
    </div>

    <!-- Aucune promo active -->
    <div v-else-if="!promotionStore.currentFlashSale" class="promo-state">
      Aucune vente flash en cours.
    </div>

    <!-- Carrousel des produits flash -->
    <template v-else>
      <div class="category__container" ref="scrollContainer" @scroll="handleScroll">
        <promoproductcard
          v-for="(product, index) in promotionStore.currentFlashSale.products"
          :key="product.id ?? index"
          :product="product"
          @add-to-cart="addToCart"
        />
      </div>

      <div class="carousel-indicators">
        <span 
          v-for="(product, index) in promotionStore.currentFlashSale.products"
          :key="product.id ?? index"
          :class="['indicator', { active: currentIndex === index }]"
          @click="scrollToIndex(index, promotionStore.currentFlashSale.products.length)"
        ></span>
      </div>
    </template>
  </section>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import promoproductcard from '../card/promoProductCard.vue'
import morebutton from '../button/morebutton.vue';
import { useCartStore } from '../../stores/cartStore'
import { usePromotionStore } from '@/stores/promotionStore';
import type { FlashSaleSimpleProduct } from '@/stores/promotionStore';
import ProductCardSkeleton from '../card/ProductCardSkeleton.vue';

export default {
  name: 'PromotionSection',
  components: {
    ProductCardSkeleton,
    promoproductcard,
    morebutton
  },
  props: {
    title: { type: String, default: "Ventes Flash" },
    description: { type: String, default: "Offres limitées, profitez-en avant la fin !" },
    buttonLabel: { type: String, default: "Voir tous les articles" }
  },
  emits: ['view-all'],
  setup() {
    const promotionStore = usePromotionStore()
    const scrollContainer = ref<HTMLElement | null>(null)
    const currentIndex = ref(0)
    const cartStore = useCartStore()
    let resizeObserver: ResizeObserver | null = null

    // ✅ 1 skeleton sur mobile, 3 sur desktop (≥1024px)
    const skeletonCount = ref(window.innerWidth >= 1024 ? 3 : 1)
    const updateSkeletonCount = () => {
      skeletonCount.value = window.innerWidth >= 1024 ? 3 : 1
    }

    const addToCart = (product: FlashSaleSimpleProduct) => {
      cartStore.addToCart({
        id: product.id,
        name: product.name,
        price: parseFloat(product.flash_price),
        image: product.image ?? ''
      })
    }

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
      if (scrollContainer.value) scrollContainer.value.scrollLeft = 0
      currentIndex.value = 0
    }

    const handleScroll = () => {
      if (scrollContainer.value) {
        const stepWidth = getStepWidth()
        if (stepWidth > 0) {
          currentIndex.value = Math.round(scrollContainer.value.scrollLeft / stepWidth)
        }
      }
    }

    const scrollToIndex = (index: number, productLength: number) => {
      if (scrollContainer.value) {
        scrollContainer.value.scrollTo({ left: index * getStepWidth(), behavior: 'smooth' })
      }
    }

    onMounted(async () => {
      // ✅ promotionStore.loading gère l'état — pas besoin d'un isloading local
      await promotionStore.fetchCurrentFlashSale()
      setTimeout(() => setupCarousel(), 0)

      if (scrollContainer.value) {
        resizeObserver = new ResizeObserver(setupCarousel)
        resizeObserver.observe(scrollContainer.value)
      }

      window.addEventListener('resize', updateSkeletonCount)
    })

    onUnmounted(() => {
      if (resizeObserver) resizeObserver.disconnect()
      window.removeEventListener('resize', updateSkeletonCount)
    })

    return {
      promotionStore,
      skeletonCount,
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
  height: 100vh;
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

/* ✅ Skeleton container : même layout que le carrousel */
.skeleton-container {
  display: flex;
  gap: 1rem;
  padding: 1rem 0.5rem;
  overflow: hidden;
}

.skeleton-container > * {
  flex: 0 0 85%;
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

.promo-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  font-size: 0.9rem;
}

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

  .section-title { font-size: 2rem; }
  .section-description { font-size: 1rem; }

  .skeleton-container > * {
    flex: 0 0 calc(50% - 0.75rem);
  }

  .category__container {
    width: 100%;
    gap: 1.5rem;
    padding: 1.5rem 1rem;
  }

  .category__container > * {
    flex: 0 0 calc(50% - 0.75rem);
  }

  .indicator { width: 10px; height: 10px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .category-section {
    width: 100%;
    max-width: none;
    margin: 0;
    padding: 3rem 2rem;
  }

  /* ✅ 3 skeletons côte à côte sur desktop */
  .skeleton-container {
    gap: 2rem;
    padding: 0;
  }

  .skeleton-container > * {
    flex: 0 0 calc(25% - 1.5rem);
  }

  .category__container {
    width: 100%;
    gap: 2rem;
    padding: 0;
    background: transparent;
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

  .section-footer { padding: 2rem 0 0 0; }

  .carousel-indicators { display: none; }
}

@keyframes addToCart {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
</style>