<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="logo">
      <h3>Calstore</h3>
    </div>

    <div class="btn__container">
      <cartButton @click="showCartModal"/>
    </div>
  </nav>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import cartButton from '../button/cartButton.vue'
import { useCartStore } from '../../stores/cartStore'

// Définir les emits avec TypeScript
interface Emits {
  (e: 'opencart'): void
}

export default {
  name: 'Navbar',
  components: {
    cartButton,
  },
  emits: {
    opencart: null
  },
  setup(props, { emit }: { emit: Emits }) {

    const store = useCartStore()

    const showCartModal = (): void => {
      emit("opencart");
    }

    // Reactive data avec typage
    const isScrolled = ref<boolean>(false)

    // Methods avec typage
    const handleScroll = (): void => {
      isScrolled.value = window.scrollY > 10
    }

    // Lifecycle
    onMounted((): void => {
      window.addEventListener('scroll', handleScroll);
      console.log(store.cart)
    })

    onBeforeUnmount((): void => {
      window.removeEventListener('scroll', handleScroll)
    })

    // Return
    return {
      isScrolled,
      store,
      showCartModal
    }
  }
}
</script>

<style scoped>
.navbar{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  background-color: white;
  transition: box-shadow 0.3s ease;
  padding: 1rem;
}

.navbar.scrolled {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo h3{
  font-size: 1.5rem;
  font-weight: 500;
  margin: 0;
}

.nav__links{
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.btn__container{
  display:flex;
  align-items: center;
  justify-content: space-around;
  gap: 0.5rem;
}
</style>