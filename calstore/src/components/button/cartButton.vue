<template>
  <div class="cart-button-container">
    <button class="btn relative">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
      </svg>
      
      <!-- Badge -->
      <span 
        v-if="totalItems > 0" 
        class="cart-badge"
        :class="{ 'pulse-animation': shouldPulse }"
      >
        {{ totalItems > 99 ? '99+' : totalItems }}
      </span>
    </button>
  </div>
</template>

<script>
import { useCartStore } from '@/stores/cartStore'
import { storeToRefs } from 'pinia'
import { ref, watch } from 'vue';

export default {
  name: 'cartbutton',
  setup() {
    const cartStore = useCartStore()
    const { totalItems } = storeToRefs(cartStore)
    
    // Animation de pulse pour les nouveaux ajouts
    const shouldPulse = ref(false)
    
    watch(totalItems, (newVal, oldVal) => {
      if (newVal > oldVal) {
        shouldPulse.value = true
        setTimeout(() => {
          shouldPulse.value = false
        }, 1000)
      }
    })

    return {
      totalItems,
      shouldPulse
    }
  }
}
</script>

<style scoped>
.cart-button-container {
  position: relative;
  display: inline-block;
}

.btn {
  position: relative;
  padding: 0.75rem;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn:hover {
  background: #f3f4f6;
}

.btn:active {
  transform: scale(0.95);
}

.size-6 {
  width: 1.5rem;
  height: 1.5rem;
}

/* Badge style */
.cart-badge {
  position: absolute;
  top: -0.25rem;
  right: -0.25rem;
  background: #ef4444;
  color: white;
  border-radius: 9999px;
  min-width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1;
  border: 2px solid white;
  animation: bounce-in 0.3s ease;
}

/* Animation pour l'apparition du badge */
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

/* Animation de pulse pour les nouveaux ajouts */
.pulse-animation {
  animation: pulse 1s ease-in-out;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}
</style>