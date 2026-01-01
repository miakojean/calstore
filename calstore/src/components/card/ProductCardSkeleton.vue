<template>
  <div class="product-card-skeleton">
    <div class="skeleton-image"></div>
    <div class="skeleton-info">
      <div class="skeleton-text skeleton-title"></div>
      <div class="skeleton-text skeleton-line-1"></div>
      <div class="skeleton-text skeleton-line-2"></div>
      <div class="skeleton-footer">
        <div class="skeleton-price"></div>
        <div class="skeleton-button"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProductCardSkeleton',
});
</script>

<style scoped>
@keyframes pulse-bg {
  0% {
    background-color: #e0e0e0;
  }
  50% {
    background-color: #d4d4d4;
  }
  100% {
    background-color: #e0e0e0;
  }
}

.product-card-skeleton {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  width: 100%;
}

.skeleton-image {
  padding-top: 100%; /* Aspect ratio 1:1 */
  background-color: #e0e0e0;
  animation: pulse-bg 1.5s infinite ease-in-out;
}

.skeleton-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: space-between;
}

.skeleton-text {
  background-color: #e0e0e0;
  border-radius: 0.25rem;
  animation: pulse-bg 1.5s infinite ease-in-out;
  margin-bottom: 0.75rem;
}

.skeleton-title {
  width: 70%;
  height: 1.25rem;
}

.skeleton-line-1 {
  width: 90%;
  height: 0.875rem;
}

.skeleton-line-2 {
  width: 60%;
  height: 0.875rem;
}

.skeleton-footer {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.skeleton-price {
  width: 40%;
  height: 1.5rem;
  background-color: #e0e0e0;
  border-radius: 0.25rem;
  animation: pulse-bg 1.5s infinite ease-in-out;
}

.skeleton-button {
  width: 30%;
  height: 2.5rem;
  background-color: #e0e0e0;
  border-radius: 1.25rem;
  animation: pulse-bg 1.5s infinite ease-in-out;
}
</style>
