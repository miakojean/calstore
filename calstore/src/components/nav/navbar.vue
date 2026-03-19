<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    
    <div class="logo">
      <h3>Calstore</h3>
    </div>

    <transition name="mobile-menu">

      <div class="nav__links" :class="{'mobile-active': isOpen}" v-show="isOpen">
        <RouterLink to="/">Accueil</RouterLink>
        
        <div 
          class="categories-container"
          @mouseenter="handleMouseEnter"
          @mouseleave="handleMouseLeave"
        >
          <RouterLink 
            to="/categories" 
            class="categories-link"
            @click.prevent="{handleCategoriesClick}"
          >
            Catégories
            <span class="dropdown-arrow">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
              </svg>
            </span>
          </RouterLink>
          
          <transition name="dropdown">
            <div 
              v-if="showDropdown" 
              class="dropdown-menu"
              @mouseenter="handleMouseEnter"
              @mouseleave="handleMouseLeave"
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
      <hamburgerButton @click="openHamburgerMenu"/>
    </div>
  </nav>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { RouterLink } from 'vue-router'
// MODIFICATION: Import correct basé sur votre fichier categoryStore.ts
import { useCategoryStore } from '../../stores/categoryStore' 
import cartButton from '../button/cartButton.vue'
import { useCartStore } from '../../stores/cartStore'
import researchinput from '../input/researchinput.vue'
import hamburgerButton from '../button/hamburgerButton.vue'

// Interfaces locales (peuvent être importées du store si besoin)
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

    const isOpen = ref(false);

    const closeMenu = () => {
      isOpen.value = false;
      document.body.style.overflow = '';
    };

    const store = useCartStore()
    // MODIFICATION: Utilisation du bon store
    const categoryStore = useCategoryStore()
    
    // État du dropdown
    const showDropdown = ref<boolean>(false)
    const dropdownTimeout = ref<NodeJS.Timeout | null>(null)

    // Récupérer les catégories depuis le store
    const categories = computed(() => {
      // Cast en any si les types ne matchent pas parfaitement entre le store et le composant
      return (categoryStore.categories || []) as any[]
    })

    // Computed pour le loading state
    const isLoading = computed(() => {
      return categoryStore.loadingStates && categoryStore.loadingStates['all']
    })

    const error = computed(() => categoryStore.error)

    // Méthodes
    const showCartModal = (): void => {
      emit("opencart")
    }

    // MODIFICATION : Nouvelle logique pour le survol
    const handleMouseEnter = (): void => {
      // Annuler la fermeture si elle était prévue (debounce)
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
        dropdownTimeout.value = null
      }
      
      showDropdown.value = true

      // LAZY LOADING : Fetch seulement si vide et pas en cours de chargement
      if (categoryStore.categories.length === 0 && !isLoading.value) {
        // Utilisation de la méthode fetchAllCategories définie dans categoryStore.ts
        categoryStore.fetchAllCategories()
      }
    }

    const handleMouseLeave = (): void => {
      // Délai pour éviter la fermeture trop rapide (meilleure UX)
      dropdownTimeout.value = setTimeout(() => {
        showDropdown.value = false
      }, 300)
    }

    const handleCategoriesClick = (): void => {
      if (window.innerWidth < 768) {
        // Sur mobile, le click toggle le menu et lance le fetch si besoin
        if (!showDropdown.value) {
           handleMouseEnter()
        } else {
           showDropdown.value = false
        }
      }
    }

    const closeDropdown = (): void => {
      showDropdown.value = false
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
      }
    }

    const cancelMouseLeave = (): void => {
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
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
      
      // SUPPRESSION : On ne charge plus automatiquement au montage
      // if (categoryStore.categories.length === 0) { ... }
    })

    onBeforeUnmount((): void => {
      window.removeEventListener('scroll', handleScroll)
      if (dropdownTimeout.value) {
        clearTimeout(dropdownTimeout.value)
      }
    })

    return {
      isOpen,
      isScrolled,
      store,
      categoryStore, // Retourné pour accès template si besoin
      showCartModal,
      showDropdown,
      categories,
      isLoading,
      error,
      openHamburgerMenu,
      handleCategoriesClick,
      closeDropdown,
      handleMouseEnter, // Nouvelle méthode retournée
      handleMouseLeave,
      cancelMouseLeave
    }
  }
}
</script>

<style scoped>

/* For mobile */

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

/* Container des catégories */
.categories-container {
  position: relative;
  display: inline-block;
  height: 100%; /* Assure que le hover ne se perd pas entre le lien et le menu */
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

.dropdown-arrow {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
}

.categories-container:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* Dropdown Menu */
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
  max-height: 70vh; /* Sécurité pour ne pas dépasser l'écran */
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

/* Sous-catégories */
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

/* Animation */
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

/* Animation personnalisée */
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

/* Responsive */
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
/* À ajouter temporairement pour le test */
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