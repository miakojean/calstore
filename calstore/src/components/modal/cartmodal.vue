<template>
  <div>
    <div 
      v-if="isOpen" 
      class="cart-modal-overlay" 
      @click="closeModal"
      :class="{ 'closing': isClosing }"
    >
      <div 
        class="cart-modal-content" 
        @click.stop
        :class="{ 'closing': isClosing }"
      >
        <div class="cart-header">
          <div class="drag-handle"></div>
          <div class="cart-title">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                </svg> 
                Mon Panier
            </h2>
            <span class="item-count">{{ totalItems }} article{{ totalItems > 1 ? 's' : '' }}</span>
          </div>
          <button class="close-icon" @click="closeModal">x</button>
        </div>

        <div class="cart-body">
          <div v-if="isEmpty" class="empty-cart">
            <div class="empty-icon">🛒</div>
            <h3>Votre panier est vide</h3>
            <p>Ajoutez des articles pour commencer vos achats</p>
            <button class="continue-shopping" @click="closeModal">
              Continuer mes achats
            </button>
          </div>

          <template v-else>
            <div class="cart-items">
              <div class="items-list">
                <div 
                  v-for="item in cart" 
                  :key="item.id"
                  class="cart-item"
                >
                  <img
                    :src="item.image || '/pic/placeholder-product.jpg'"
                    :alt="item.name"
                    class="item-image"
                  >

                  <div class="item-details">
                    <h4 class="item-name">{{ item.name }}</h4>
                    <p class="item-price">{{ item.price }} FCFA</p>

                    <div class="quantity-controls">
                      <button 
                        class="qty-btn" 
                        @click="decreaseQuantity(item.id)"
                        :disabled="item.quantity <= 1"
                      >
                        -
                      </button>
                      <span class="quantity">{{ item.quantity }}</span>
                      <button 
                        class="qty-btn" 
                        @click="increaseQuantity(item.id)"
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div class="item-total">
                    <span class="total-price">{{ (item.price * item.quantity).toFixed(2) }} FCFA</span>
                    <button 
                      class="remove-btn"
                      @click="removeFromCart(item.id)"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="order-summary">
              <div class="summary-line">
                <span>Sous-total</span>
                <span>{{ formattedTotalPrice }} FCFA</span>
              </div>
              <div class="summary-line">
                <span>Livraison</span>
                <span>Gratuite</span>
              </div>
              <div class="summary-line total">
                <span>Total</span>
                <span class="final-price">{{ formattedTotalPrice }} FCFA</span>
              </div>
            </div>
          </template>
        </div>

        <div class="cart-footer" v-if="!isEmpty">
          <checkoutButton 
            :label="`Commander • ${formattedTotalPrice} FCFA`" 
            @handleClicked="proceedToCheckout"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, ref } from 'vue'
import { useCartStore } from '../../stores/cartStore'
import checkoutButton from '../button/checkoutButton.vue';
import { useRouter } from 'vue-router';

export default {
  name: 'CartModal',
  components:{
    checkoutButton
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const cartStore = useCartStore()
    const isClosing = ref(false)
    const router = useRouter();

    const closeModal = () => {
      isClosing.value = true
      setTimeout(() => {
        emit('close')
        isClosing.value = false
      }, 300)
    }

    // Procéder au paiement

    const step = ref(1) // Première étape du paiement
    const proceedToCheckout = () => {
      console.log('Afficher les données du panier non normalisé:', cartStore.cartUnormaled);
      closeModal()
      router.push('/cart-checkout');
    }

    // Formater le prix total pour l'affichage
    const formattedTotalPrice = computed(() => {
      return cartStore.totalPrice.toFixed(2)
    })

    return {
      router,
      closeModal,
      proceedToCheckout,
      formattedTotalPrice,
      cart: computed(() => cartStore.cart), // Utiliser un computed pour garantir la réactivité
      totalItems: computed(() => cartStore.totalItems),
      totalPrice: computed(() => cartStore.totalPrice),
      isEmpty: computed(() => cartStore.isEmpty),
      isClosing,
      increaseQuantity: cartStore.increaseQuantity,
      decreaseQuantity: cartStore.decreaseQuantity,
      removeFromCart: cartStore.removeFromCart
    }
  }
}
</script>

<style scoped>
/* Overlay */
.cart-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  animation: fadeIn 0.3s ease;
}

.cart-modal-overlay.closing {
  animation: fadeOut 0.3s ease;
}

/* Contenu de la modale */
.cart-modal-content {
  background: white;
  width: 100%;
  height: 85vh;
  border-top-left-radius: 1.5rem;
  border-top-right-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
}

.cart-modal-content.closing {
  animation: slideDown 0.3s ease;
}

/* Header */
.cart-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.drag-handle {
  width: 40px;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
}

.cart-title h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.size-6 {
  width: 1.5rem;
  height: 1.5rem;
}

.item-count {
  color: #666;
  font-size: 0.9rem;
}

.close-icon {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0.25rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.close-icon:hover {
  background: #f5f5f5;
}

/* Corps du panier */
.cart-body {
  flex: 1;
  overflow-y: auto;
  padding: 0 1.5rem;
}

/* Panier vide */
.empty-cart {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-cart h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.empty-cart p {
  margin: 0 0 1.5rem 0;
}

.continue-shopping {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.continue-shopping:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

/* Liste des articles */
.cart-items {
  padding: 1rem 0;
}

.cart-item {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 0.5rem;
  background: #f8f9fa;
}

.item-details {
  flex: 1;
}

.item-name {
  margin: 0 0 0.25rem 0;
  font-size: 0.95rem;
  font-weight: 500;
  color: #333;
}

.item-price {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #007bff;
  font-weight: 600;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.qty-btn:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #007bff;
}

.qty-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.quantity {
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}

.item-total {
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.total-price {
  font-weight: 600;
  color: #1a1a1a;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  opacity: 0.6;
  padding: 0.25rem;
  transition: opacity 0.2s ease;
}

.remove-btn:hover {
  opacity: 1;
}

/* Résumé de commande */
.order-summary {
  background: #f8f9fa;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-top: 1.5rem;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.summary-line.total {
  border-top: 1px solid #ddd;
  padding-top: 0.75rem;
  margin-top: 0.75rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.final-price {
  color: #007bff;
}

/* Footer */
.cart-footer {
  padding: 1.5rem;
  border-top: 1px solid #f0f0f0;
  background: white;
}

.checkout-btn {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.btn-arrow {
  font-size: 1.2rem;
}

/* Animations */
@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(100%);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* Scroll personnalisé */
.cart-body::-webkit-scrollbar {
  width: 4px;
}

.cart-body::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.cart-body::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.cart-body::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Responsive */
@media (min-width: 768px) {
  .cart-modal-overlay {
    align-items: center;
    justify-content: center;
  }

  .cart-modal-content {
    width: 90%;
    max-width: 500px;
    height: auto;
    max-height: 80vh;
    border-radius: 1rem;
    animation: scaleUp 0.3s ease;
  }

  .cart-modal-content.closing {
    animation: scaleDown 0.3s ease;
  }

  @keyframes scaleUp {
    from {
      transform: scale(0.9) translateY(20px);
      opacity: 0;
    }
    to {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
  }

  @keyframes scaleDown {
    from {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
    to {
      transform: scale(0.9) translateY(20px);
      opacity: 0;
    }
  }
}
</style>