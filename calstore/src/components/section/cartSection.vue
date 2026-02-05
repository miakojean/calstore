<template>
  <div class="cart-section flex flex-col gap-6">
    <!-- Liste des articles -->
    <h3>Mon Panier</h3>
    <div class="items-list" v-if="!cartStore.isLoading" >
      <div 
        v-for="item in cartStore.cart" 
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
          <p class="item-price">{{ formatPrice(item.price) }} FCFA</p>

          <div class="quantity-controls">
            <button 
              class="qty-btn" 
              @click="decreaseQuantity(item)"
              :disabled="item.quantity <= 1"
            >
              -
            </button>
            <span class="quantity">{{ item.quantity }}</span>
            <button 
              class="qty-btn" 
              @click="increaseQuantity(item)"
              :disabled="item.maxStock && item.quantity >= item.maxStock"
            >
              +
            </button>
          </div>
        </div>

        <div class="item-total">
          <span class="total-price">{{ formatPrice(item.price * item.quantity) }} FCFA</span>
          <button 
            class="remove-btn"
            @click="removeItem(item.id)"
          >
            🗑️
          </button>
        </div>
      </div>

      <!-- Message panier vide -->
      <div v-if="cartStore.isEmpty" class="empty-cart">
        <p>Votre panier est vide</p>
        <p class="empty-message">Ajoutez des produits pour commencer vos achats</p>
      </div>
    </div>

    <!-- Résumé de commande (seulement si le panier n'est pas vide) -->
    <div v-if="!cartStore.isEmpty" class="order-summary">
      <h3>Résumé de la commande</h3>
      
      <div class="summary-line">
        <span>Sous-total ({{ cartStore.totalItems }} article{{ cartStore.totalItems > 1 ? 's' : '' }})</span>
        <span>{{ formatPrice(cartStore.totalPrice) }} FCFA</span>
      </div>
      
      <div class="summary-line">
        <span>Livraison</span>
        <span>Gratuite</span>
      </div>
      
      <div class="summary-line total">
        <span>Total</span>
        <span class="final-price">{{ formatPrice(cartStore.totalPrice) }} FCFA</span>
      </div>

    </div>

    <!-- Skeleton de chargement -->
    <div v-if="cartStore.isLoading" class="w-full">
      <cartSkeleton />
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore';
import cartSkeleton from './cartSkeleton.vue';


const cartStore = useCartStore();

// Formatage du prix
const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-FR').format(price);
};

// Augmenter la quantité
const increaseQuantity = async (item) => {
  await cartStore.increaseQuantity(item.id);
};

// Diminuer la quantité
const decreaseQuantity = async (item) => {
  await cartStore.decreaseQuantity(item.id);
};

// Supprimer un article
const removeItem = async (itemId) => {
  await cartStore.removeFromCart(itemId);
};
</script>

<style scoped>
.cart-section {
  width: 100%;
}

.items-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-item {
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 12px;
  background: linear-gradient(180deg,#fff,#fbfdff);
  border-radius: 12px;
  border: 1px solid #f1f5f9;
  transition: transform 0.2s ease;
}

.cart-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.item-image {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: 10px;
  background: #f3f7fa;
  flex-shrink: 0;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.item-name {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 600;
  color: #071033;
}

.item-price {
  margin: 0;
  color: #0ea5e9;
  font-weight: 700;
  font-size: 0.9rem;
}

.quantity-controls {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.qty-btn {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: 1px solid #e6eef6;
  background: white;
  display: grid;
  place-items: center;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.qty-btn:hover:not(:disabled) {
  background: #f0f7ff;
  border-color: #0ea5e9;
}

.qty-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.quantity {
  min-width: 28px;
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
}

.item-total {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.total-price {
  font-weight: 700;
  color: #0f172a;
  font-size: 1rem;
}

.remove-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #ef4444;
  font-size: 1.05rem;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.remove-btn:hover {
  background: rgba(239, 68, 68, 0.1);
}

.empty-cart {
  width: 100%;
  text-align: center;
  padding: 4rem 1rem;
  color: #6b7280;
}

.empty-cart p {
  margin: 0;
  font-size: 1rem;
}

.empty-cart .empty-message {
  font-size: 0.9rem;
  margin-top: 8px;
  color: #9ca3af;
}

.order-summary {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-summary h3 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  color: #0f172a;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  color: #6b7280;
  font-size: 0.95rem;
}

.summary-line.total {
  border-top: 1px dashed #e6eef6;
  padding-top: 10px;
  font-weight: 700;
  color: #071033;
  font-size: 1.05rem;
}

.final-price {
  color: #0369a1;
  font-weight: 800;
}

/* Responsive */
@media (max-width: 880px) {
  .cart-item {
    padding: 10px;
    gap: 12px;
  }
  
  .item-image {
    width: 60px;
    height: 60px;
  }
  
  .item-name {
    font-size: 0.92rem;
  }
  
  .order-summary {
    padding: 14px;
  }
}
</style>