<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    
    <div class="logo">
      <h3>Calstore</h3>
    </div>

    <transition name="mobile-menu">
      <div class="nav__links" :class="{'mobile-active': isOpen}" v-show="showMenu">
        <RouterLink to="/">Accueil</RouterLink>
        
        <div 
          class="categories-container"
          ref="categoriesContainerRef"
          @mouseenter="isDesktop && handleMouseEnter()"
          @mouseleave="isDesktop && handleMouseLeave()"
        >
          <!-- Desktop : lien cliquable vers /categories -->
          <RouterLink 
            v-if="isDesktop"
            to="/categories" 
            class="categories-link"
          >
            Catégories
            <span class="dropdown-arrow">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
              </svg>
            </span>
          </RouterLink>

          <!-- Tablette / Mobile : bouton qui déroule uniquement -->
          <button
            v-else
            class="categories-link categories-btn"
            :class="{ 'arrow-open': showDropdown }"
            @click="handleCategoriesClick"
          >
            Catégories
            <span class="dropdown-arrow">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
              </svg>
            </span>
          </button>
          
          <transition name="dropdown">
            <div 
              v-if="showDropdown" 
              class="dropdown-menu"
              ref="dropdownRef"
              @mouseenter="isDesktop && handleMouseEnter()"
              @mouseleave="isDesktop && handleMouseLeave()"
            >
              <div class="dropdown-content">
                
                <div v-if="isLoading" class="dropdown-item">
                  <span class="dropdown-link" style="color: #888; cursor: default;">
                    Chargement...
                  </span>
                </div>

                <div v-else-if="categories.length === 0 && !error" class="dropdown-item">
                  <span class="dropdown-link" style="cursor: default;">
                    Aucune catégorie
                  </span>
                </div>

                <div 
                  v-else
                  v-for="category in categories" 
                  :key="category.id"
                  class="dropdown-item"
                >
                  <RouterLink 
                    :to="`/categories/${category.slug}`"
                    class="dropdown-link"
                    @click="closeDropdown(); $emit('handle-category', category)"
                  >
                    {{ category.name }}
                  </RouterLink>
                  
                  <div 
                    v-if="category.subcategories && category.subcategories.length"
                    class="subcategories"
                  >
                    <RouterLink
                      v-for="sub in category.subcategories"
                      :key="sub.id"
                      :to="{name:category, params:sub.name}"
                      class="subcategory-link"
                      @click="closeDropdown"
                    >
                      {{ sub.name }}
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>
        
        <RouterLink to="/about">Promotions</RouterLink>
        <RouterLink to="/about">À propos</RouterLink>
        <RouterLink to="/contact">Contact</RouterLink>
      </div>
    </transition>

    <div class="btn__container">
      <researchinput/>
      <cartButton @click="showCartModal"/>
      <hamburgerButton @click="isOpen = !isOpen"/>
    </div>
  </nav>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useCategoryStore } from '../../stores/categoryStore' 
import cartButton from '../button/cartButton.vue'
import { useCartStore } from '../../stores/cartStore'
import researchinput from '../input/researchinput.vue'
import hamburgerButton from '../button/hamburgerButton.vue'

// Interfaces
interface Subcategory {
  id: number | string
  name: string
  slug: string
  category_id: number | string
}

interface Category {
  id: number | string
  name: string
  slug: string
  subcategories?: Subcategory[]
}

interface Emits {
  (e: 'opencart'): void,
  (e: 'handle-category'): void
}

export default {
  name: 'Navbar',
  components: {
    cartButton,
    researchinput,
    hamburgerButton
  },
  
  emits: ['opencart', 'handle-category'],
  
  setup(props, { emit }: { emit: Emits }) {

    const isOpen = ref(false)

    const closeMenu = () => {
      isOpen.value = false
      document.body.style.overflow = ''
    }

    // ✅ Seuil relevé à 1024px : en dessous = tablette/mobile → clic
    const DESKTOP_BREAKPOINT = 1024
    const isDesktop = ref(window.innerWidth >= DESKTOP_BREAKPOINT)

    const updateIsDesktop = () => {
      isDesktop.value = window.innerWidth >= DESKTOP_BREAKPOINT
      // Fermer le dropdown lors d'un changement de breakpoint
      if (isDesktop.value) {
        closeDropdown()
      }
    }

    const showMenu = computed(() => isDesktop.value || isOpen.value)

    const store = useCartStore()
    const categoryStore = useCategoryStore()
    
    const showDropdown = ref<boolean>(false)
    const dropdownTimeout = ref<NodeJS.Timeout | null>(null)
    const dropdownRef = ref<HTMLElement | null>(null)
    // ✅ Référence sur le conteneur entier (bouton + menu) pour le clic extérieur
    const categoriesContainerRef = ref<HTMLElement | null>(null)

    const categories = computed(() => {
      return (categoryStore.categories || []) as any[]
    })

    const isLoading = computed(() => {
      return categoryStore.loadingStates && categoryStore.loadingStates['all']
    })

    const error = computed(() => categoryStore.error)

    const showCartModal = (): void => {
      emit("opencart")
    }

    const handleMouseEnter = (): void => {
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
        dropdownTimeout.value = null
      }
      
      showDropdown.value = true

      if (categoryStore.categories.length === 0 && !isLoading.value) {
        categoryStore.fetchAllCategories()
      }
    }

    const handleMouseLeave = (): void => {
      dropdownTimeout.value = setTimeout(() => {
        showDropdown.value = false
      }, 300)
    }

    const handleCategoriesClick = (): void => {
      // ✅ Sur tablette/mobile : toggle au clic
      if (!isDesktop.value) {
        if (!showDropdown.value) {
          handleMouseEnter()
        } else {
          closeDropdown()
        }
      }
      // Sur desktop : le hover gère tout, le clic ne fait rien
    }

    const closeDropdown = (): void => {
      showDropdown.value = false
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
        dropdownTimeout.value = null
      }
    }

    const cancelMouseLeave = (): void => {
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
      }
    }

    // ✅ Clic extérieur : on vérifie le conteneur entier (bouton + dropdown)
    const handleClickOutside = (event: MouseEvent) => {
      if (
        !isDesktop.value &&
        categoriesContainerRef.value &&
        !categoriesContainerRef.value.contains(event.target as Node)
      ) {
        closeDropdown()
      }
    }

    // Scroll
    const isScrolled = ref<boolean>(false)
    const handleScroll = (): void => {
      isScrolled.value = window.scrollY > 10
    }

    // Lifecycle
    onMounted((): void => {
      window.addEventListener('scroll', handleScroll)
      window.addEventListener('resize', updateIsDesktop)
      document.addEventListener('click', handleClickOutside)
      updateIsDesktop()
    })

    onBeforeUnmount((): void => {
      window.removeEventListener('scroll', handleScroll)
      window.removeEventListener('resize', updateIsDesktop)
      document.removeEventListener('click', handleClickOutside)
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
      }
    })

    return {
      isOpen,
      isScrolled,
      store,
      categoryStore,
      showMenu,
      showCartModal,
      showDropdown,
      categories,
      isLoading,
      error,
      handleCategoriesClick,
      closeDropdown,
      handleMouseEnter,
      handleMouseLeave,
      cancelMouseLeave,
      dropdownRef,
      categoriesContainerRef,
      isDesktop
    }
  }
}
</script>

<style scoped>
.navbar {
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

.logo h3 {
  font-size: 1.5rem;
  font-weight: 500;
  margin: 0;
}

.nav__links {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  position: relative;
}

.categories-container {
  position: relative;
  display: inline-block;
  height: 100%;
}

.categories-link {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  padding: 8px 0;
}

/* Reset natif du <button> pour qu'il ressemble au lien */
.categories-btn {
  background: none;
  border: none;
  font-size: inherit;
  font-family: inherit;
  cursor: pointer;
}

.dropdown-arrow {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
}

/* ✅ Rotation de la flèche au hover (desktop) ET au clic (tablette/mobile) */
.categories-container:hover .dropdown-arrow,
.categories-link.arrow-open .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 220px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  margin-top: 8px;
  z-index: 1001;
  overflow: hidden;
  animation: slideDown 0.2s ease;
}

.dropdown-content {
  padding: 12px 0;
  max-height: 70vh;
  overflow-y: auto;
}

.dropdown-item {
  position: relative;
}

.dropdown-link {
  display: block;
  padding: 10px 20px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.dropdown-link:hover {
  background-color: #f5f5f5;
}

.subcategories {
  padding-left: 20px;
  border-left: 2px solid #eee;
  margin-left: 20px;
  margin-top: 5px;
  margin-bottom: 5px;
}

.subcategory-link {
  display: block;
  padding: 8px 20px;
  text-decoration: none;
  color: #666;
  font-size: 0.9em;
  transition: color 0.2s ease;
}

.subcategory-link:hover {
  color: #007bff;
  background-color: transparent;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.3s ease;
  transform-origin: top center;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scaleY(0.8);
}

.btn__container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 0.5rem;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ✅ Tablette (769px – 1023px) : menu visible, dropdown en position statique */
@media (max-width: 1023px) and (min-width: 769px) {
  .categories-container {
    position: static;
  }

  .dropdown-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    min-width: auto;
    border-radius: 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
}

/* Mobile (≤ 768px) */
@media (max-width: 768px) {
  .nav__links {
    display: none;
  }

  .nav__links.mobile-active {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background-color: white;
    padding: 1rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    z-index: 999;
    transition: ease-in 0.3s;
  }

  .categories-container {
    position: static;
  }
  
  .dropdown-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    min-width: auto;
    border-radius: 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
}

/* Sur desktop, on désactive la transition mobile-menu */
@media (min-width: 1024px) {
  .mobile-menu-enter-active,
  .mobile-menu-leave-active {
    transition: none !important;
  }
}

/* Dark mode temporaire */
@media (prefers-color-scheme: dark) {
  .navbar,
  .navbar * {
    color: white;
  }
  
  .navbar {
    background-color: #1a1a1a;
  }
}
</style>