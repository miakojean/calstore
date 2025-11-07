<template>
  <section>
    <h4>{{ title }}</h4>
    <p>Découvrir notre panoplie de chaussures</p>
    <div class="category__container" ref="scrollContainer" @scroll="handleScroll">
      <productcard v-for="(card, index) in cards" :key="index" />
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

    <seconbutton label="Voir tous les articles"/>
  </section>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import productcard from '../card/productcard.vue'
import seconbutton from '../button/seconbutton.vue';

export default {
  name: 'CategorySection',
  components: {
    productcard,
    seconbutton,
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

    // Methods
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

    // Lifecycle
    onMounted(() => {
      setupCarousel()
    })

    // Return everything that should be available in template
    return {
      scrollContainer,
      currentIndex,
      cards,
      handleScroll,
      scrollToIndex
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
</style>