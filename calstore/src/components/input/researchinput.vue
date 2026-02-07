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
        @input="onSearch"
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
      <div v-if="showResults" class="search-results">
        <p>Bienvenue au pays mon fils</p>
        <!-- Ici tu pourras ajouter tes résultats d'API -->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue';
import { useQueryStore } from '@/stores/queryStore';

export default {
  props: {
    modelValue: {
      type: String,
      default: ""
    }
  },

  emits: ['update:modelValue', 'search'],

  setup(props, { emit }) {
    // State
    const isExpanded = ref(false);
    const searchQuery = ref<string>(props.modelValue || '');
    const showResults = ref(false);
    const searchInput = ref<HTMLInputElement | null>(null);
    const searchContainer = ref<HTMLDivElement | null>(null);
    const queryStore = useQueryStore()

    // Méthodes
    const expandSearch = () => {
      isExpanded.value = true;
      showResults.value = false;
      
      // Focus sur l'input après l'expansion
      nextTick(() => {
        searchInput.value?.focus();
      });
    };

    const collapseSearch = () => {
      if (!searchQuery.value) {
        isExpanded.value = false;
      }
      showResults.value = false;
    };

    const onSearch = () => {
      emit('update:modelValue', searchQuery.value);
      
      // Afficher les résultats si recherche non vide
      showResults.value = searchQuery.value.length > 0;
    };

    const performSearch = () => {
      if (searchQuery.value.trim()) {
        emit('search', searchQuery.value);
        // Ici tu pourras appeler ton API Django
        console.log('Recherche envoyée:', searchQuery.value);
      }
    };

    const onBlur = () => {
      // Ne pas fermer si l'utilisateur clique sur les résultats
      setTimeout(() => {
        if (!searchQuery.value) {
          isExpanded.value = false;
        }
      }, 200);
    };

    // Fermer si on clique en dehors
    const handleClickOutside = (event: MouseEvent) => {
      if (
        searchContainer.value && 
        !searchContainer.value.contains(event.target as Node) &&
        !searchQuery.value
      ) {
        isExpanded.value = false;
        showResults.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    // Watch pour synchroniser avec le parent
    const unwatch = watch(() => props.modelValue, (newValue) => {
      searchQuery.value = newValue;
      queryStore.makeProductQuery(newValue)
    });

    return {
      // State
      isExpanded,
      searchQuery,
      showResults,
      searchInput,
      searchContainer,
      queryStore,
      unwatch,
      
      // Méthodes
      expandSearch,
      collapseSearch,
      onSearch,
      performSearch,
      onBlur
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
  min-width: 200px;
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
  padding: 12px;
  margin-top: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  animation: fadeIn 0.2s ease;
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

/* Responsive */
@media (max-width: 768px) {
  .search-input {
    min-width: 150px;
    max-width: calc(100vw - 100px);
  }
  
  .search-results {
    width: 100vw;
    max-width: 300px;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>