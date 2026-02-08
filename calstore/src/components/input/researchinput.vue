<template>
  <div class="search-container">
    <!-- État 1 : Icône seule (par défaut) -->
    <div 
      v-if="!isExpanded"
      class="search-icon"
      @click.stop="expandSearch"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="search-svg">
        <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
      </svg>
    </div>

    <!-- État 2 : Champ de recherche étendu -->
    <div 
      v-else
      class="search-expanded"
      ref="searchContainer"
    >
      <input
        ref="searchInput"
        type="text"
        placeholder="Trouver un produit..."
        v-model="searchQuery"
        @input="handleInput"
        @blur="onBlur"
        @keyup.enter="performSearch"
        @keyup.esc="collapseSearch"
        class="search-input"
      />
      
      <!-- Bouton pour fermer -->
      <button @click="collapseSearch" class="close-btn">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="close-svg">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Résultats de recherche -->
      <div v-if="showResults && queryStore.results.length > 0" class="search-results">
        <div 
          v-for="product in queryStore.results" 
          :key="product.id" 
          class="product-result"
          @click="goToProduct(product)"
        >
          <div class="product-left">
            <!-- Image du produit -->
            <div class="product-image">
              <img 
                v-if="getImageUrl(product)" 
                :src="getImageUrl(product)" 
                :alt="product.name"
                class="product-img"
                @error="handleImageError"
                loading="lazy"
              />
              <div v-else class="no-image">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="no-image-svg">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                </svg>
              </div>
            </div>
            
            <!-- Informations du produit -->
            <div class="product-info">
              <h4 class="product-name">{{ product.name }}</h4>
              <div class="product-price">{{ formatPrice(product.price) }}</div>
              <div 
                class="stock-status"
                :class="{ 'in-stock': product.stock > 0, 'out-of-stock': product.stock <= 0 }"
              >
                <span class="stock-dot"></span>
                {{ product.stock > 0 ? 'Disponible' : 'Rupture de stock' }}
                <span v-if="product.stock > 0" class="stock-quantity">({{ product.stock }} en stock)</span>
              </div>
            </div>
          </div>
          
          <!-- Panier à droite -->
          <div class="product-right">
            <button 
              class="add-to-cart-btn"
              :disabled="product.stock <= 0"
              @click.stop="addToCart(product)"
              :title="product.stock > 0 ? 'Ajouter au panier' : 'Produit indisponible'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="cart-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
              </svg>
            </button>
          </div>
        </div>
        
        <div v-if="queryStore.isLoading" class="loading-indicator">
          <div class="spinner"></div>
          Chargement...
        </div>
      </div>
      
      <div v-else-if="showResults && searchQuery && !queryStore.isLoading" class="search-results">
        <div class="no-results">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="no-results-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
          <p>Aucun résultat trouvé pour "{{ searchQuery }}"</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useQueryStore } from '../../stores/queryStore';
import { useRouter } from 'vue-router';
import { useCategoryStore } from '../../stores/categoryStore';
import { useCartStore } from '../../stores/cartStore';

export default {
  props: {
    modelValue: {
      type: String,
      default: ""
    }
  },

  emits: ['update:modelValue', 'search', 'add-to-cart'],

  setup(props, { emit }) {
    const router = useRouter();
    
    // State
    const isExpanded = ref(false);
    const searchQuery = ref<string>(props.modelValue || '');
    const showResults = ref(false);
    const searchInput = ref<HTMLInputElement | null>(null);
    const searchContainer = ref<HTMLDivElement | null>(null);
    const queryStore = useQueryStore();
    const categoryStore = useCategoryStore();
    const cartStore = useCartStore();
    let debounceTimer: ReturnType<typeof setTimeout> | null = null;

    // Configuration de l'URL backend
    const backendBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

    // Méthodes
    const expandSearch = () => {
      isExpanded.value = true;
      showResults.value = false;
      
      // Focus sur l'input après l'expansion
      setTimeout(() => {
        searchInput.value?.focus();
      }, 100);
    };

    const collapseSearch = () => {
      searchQuery.value = '';
      emit('update:modelValue', '');
      isExpanded.value = false;
      showResults.value = false;
      queryStore.results = [];
    };

    const handleInput = () => {
      emit('update:modelValue', searchQuery.value);
      
      // Debounce pour éviter les requêtes multiples
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }
      
      if (searchQuery.value.trim().length === 0) {
        showResults.value = false;
        queryStore.results = [];
        return;
      }
      
      debounceTimer = setTimeout(() => {
        if (searchQuery.value.trim().length > 0) {
          queryStore.makeProductQuery(searchQuery.value.trim());
          showResults.value = true;
        }
      }, 300);
    };

    const performSearch = () => {
      if (searchQuery.value.trim()) {
        emit('search', searchQuery.value);
        console.log('Recherche envoyée:', searchQuery.value);
      }
    };

    const onBlur = () => {
      // Donner le temps de cliquer sur les résultats
      setTimeout(() => {
        if (!searchQuery.value.trim()) {
          isExpanded.value = false;
          showResults.value = false;
        }
      }, 300);
    };

    const formatPrice = (price: number) => {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 2
      }).format(price);
    };

    const getImageUrl = (product: any) => {
      // Essayez différents champs d'image possibles
      const imageField = product.main_image_url || product.image_url || product.image || product.thumbnail;
      
      if (!imageField) return null;
      
      // Si l'URL est absolue (commence par http:// ou https://)
      if (imageField.startsWith('http://') || imageField.startsWith('https://')) {
        return imageField;
      }
      
      // Si c'est une URL relative, ajoutez le base URL du backend
      if (imageField.startsWith('/')) {
        return `${backendBaseUrl}${imageField}`;
      }
      
      // Si c'est juste un chemin relatif
      return `${backendBaseUrl}/${imageField}`;
    };

    const handleImageError = (event: Event) => {
      const img = event.target as HTMLImageElement;
      img.style.display = 'none';
      // L'élément .no-image sera affiché automatiquement grâce à v-else
    };

    const goToProduct = (product: any) => {
      if (product.id) {
        router.push(`/product/${product.id}`);
        collapseSearch();
      }
    };

    const addToCart = async (product: any) => {
      await cartStore.addToCart(product);
    };

    // Fermer si on clique en dehors
    const handleClickOutside = (event: MouseEvent) => {
      if (
        searchContainer.value && 
        !searchContainer.value.contains(event.target as Node)
      ) {
        if (!searchQuery.value.trim()) {
          isExpanded.value = false;
        }
        showResults.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }
    });

    // Watch pour synchroniser avec le parent
    watch(() => props.modelValue, (newValue) => {
      if (newValue !== searchQuery.value) {
        searchQuery.value = newValue;
        if (newValue.trim().length > 0) {
          queryStore.makeProductQuery(newValue.trim());
          showResults.value = true;
        }
      }
    });

    return {
      // State
      isExpanded,
      searchQuery,
      showResults,
      searchInput,
      searchContainer,
      queryStore,
      categoryStore,
      cartStore,
      
      // Méthodes
      expandSearch,
      collapseSearch,
      handleInput,
      performSearch,
      onBlur,
      formatPrice,
      getImageUrl,
      handleImageError,
      goToProduct,
      addToCart
    };
  }
};
</script>

<style scoped>
.search-container {
  display: inline-block;
  position: relative;
}

/* Style de l'icône */
.search-icon {
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.search-icon:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.search-svg {
  width: 24px;
  height: 24px;
  color: #666;
}

/* Style du champ étendu */
.search-expanded {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: expand 0.3s ease;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  min-width: 250px;
  transition: width 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.close-svg {
  width: 20px;
  height: 20px;
  color: #666;
}

/* Résultats de recherche */
.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 8px 0;
  margin-top: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  animation: fadeIn 0.2s ease;
  max-height: 400px;
  overflow-y: auto;
  min-width: 350px;
}

/* Structure produit */
.product-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid #f0f0f0;
  gap: 12px;
}

.product-result:hover {
  background-color: #f9f9f9;
}

.product-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0; /* Pour le text-overflow */
}

.product-image {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
  position: relative;
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  background-color: #f5f5f5; /* Couleur de fond en attendant le chargement */
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  border-radius: 4px;
  color: #999;
}

.no-image-svg {
  width: 24px;
  height: 24px;
}

.product-info {
  flex: 1;
  min-width: 0; /* Pour le text-overflow */
}

.product-name {
  font-weight: 500;
  font-size: 14px;
  margin: 0 0 4px 0;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-price {
  font-weight: 600;
  font-size: 15px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stock-status {
  display: flex;
  align-items: center;
  font-size: 12px;
  gap: 6px;
}

.stock-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.stock-status.in-stock {
  color: #27ae60;
}

.stock-status.in-stock .stock-dot {
  background-color: #27ae60;
}

.stock-status.out-of-stock {
  color: #e74c3c;
}

.stock-status.out-of-stock .stock-dot {
  background-color: #e74c3c;
}

.stock-quantity {
  color: #7f8c8d;
  font-size: 11px;
}

/* Panier à droite */
.product-right {
  flex-shrink: 0;
}

.add-to-cart-btn {
  background-color: var(--my-black-color);
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.add-to-cart-btn:hover:not(:disabled) {
  background-color: var(--my-black-color);
  transform: scale(1.1);
}

.add-to-cart-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
  opacity: 0.6;
}

.cart-icon {
  width: 18px;
  height: 18px;
}

/* Chargement */
.loading-indicator {
  padding: 16px;
  color: #666;
  text-align: center;
  font-style: italic;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Aucun résultat */
.no-results {
  padding: 24px 16px;
  text-align: center;
  color: #7f8c8d;
}

.no-results-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 12px;
  color: #bdc3c7;
}

.no-results p {
  margin: 0;
  font-size: 14px;
}

/* Animations */
@keyframes expand {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .search-input {
    min-width: 180px;
    max-width: calc(100vw - 100px);
  }
  
  .search-results {
    width: calc(100vw - 32px);
    max-width: 400px;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .product-result {
    padding: 10px 12px;
  }
  
  .product-image {
    width: 40px;
    height: 40px;
  }
}
</style>