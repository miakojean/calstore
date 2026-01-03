<template>
  <transition name="modal-slide">
    <div v-if="isOpen" class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <button class="close-btn" @click="close">&times;</button>
        <div v-if="product" class="product-details">
          <div class="product-image-container">
            <img :src="product && product.main_image_url ? product.main_image_url : (product && product.image ? ('/pic/' + product.image) : '')" :alt="product?.name" class="product-image">
          </div>
          <div class="product-info">
            <h2 class="product-name">{{ product.name }}</h2>
            <p class="product-description">{{ product.description }}</p>
            <div class="price-section">
              <span class="current-price">{{ product.price }} FCFA</span>
              <span v-if="product.originalPrice" class="original-price">{{ product.originalPrice }} FCFA</span>
            </div>
            <div v-if="product.rating" class="rating-section">
              <span class="stars">{{ getStars(product.rating) }}</span>
              <span class="review-count">({{ product.reviewCount }} avis)</span>
            </div>
            <addtocartbutton @click="addToCart" />
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import type { Product } from '../../types/Product';
import addtocartbutton from '../button/addtocartbutton.vue';

export default defineComponent({
  name: 'ProductDetailModal',
  components: {
    addtocartbutton
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    product: {
      type: Object as PropType<Product | null>,
      required: false,
      default: null,
    },
  },
  emits: ['close', 'add-to-cart'],
  methods: {
    close() {
      this.$emit('close');
    },
    addToCart() {
      if (this.product) {
        this.$emit('add-to-cart', this.product);
      }
    },
    getStars(rating: number) {
      const fullStars = '★'.repeat(Math.floor(rating));
      const emptyStars = '☆'.repeat(5 - Math.floor(rating));
      return fullStars + emptyStars;
    }
  }
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: flex-end;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  height: 100%;
  width: 650px;
  max-width: 100%;
  box-shadow: -5px 0 25px rgba(0,0,0,0.2);
  position: relative;
  overflow-y: auto;
  padding: 2rem;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 2rem;
  color: #333;
  cursor: pointer;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.product-image-container {
  width: 100%;
  border-radius: 1rem;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.product-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: #222;
}

.product-description {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

.price-section {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  font-size: 1.5rem;
}

.current-price {
  font-weight: 600;
  color: var(--primary-color, #333);
}

.original-price {
  text-decoration: line-through;
  color: #999;
  font-size: 1.1rem;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.stars {
  color: #f5a623;
  font-size: 1.1rem;
}

/* Animation */
.modal-slide-enter-active,
.modal-slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-slide-enter-from,
.modal-slide-leave-to {
  transform: translateX(100%);
}

/* Responsive */
@media (max-width: 768px) {
  .modal-overlay {
    align-items: flex-end;
  }
  .modal-content {
    width: 100%;
    height: 80%;
    border-top-left-radius: 1.5rem;
    border-top-right-radius: 1.5rem;
    transform: translateY(0);
  }
  .modal-slide-enter-from,
  .modal-slide-leave-to {
    transform: translateY(100%);
  }
}
</style>
