<template>
  <section class="brand-section">
    <div class="brand-content">
      <div class="text-content">
        <h2>{{ promotionStore.currentFlashSale?.name }}</h2>
        <p class="discount-info">
          Profitez jusqu'à <span class="highlight"> -25%</span> sur une sélection d'articles. Offre à durée limitée !
        </p>
        <div class="btn__section">
          <mainbutton/>
          <seconbutton 
            @click="() => router.push('/promotions')"
          />
        </div>
      </div>
      <div class="image-content">
        <img src="../assets/images/Copilot_20251112_142208.png" alt="Promotions de fin d'année" />
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import mainbutton from './button/mainbutton.vue';
import seconbutton from './button/seconbutton.vue';
import { usePromotionStore } from '../stores/promotionStore';
import { onMounted } from 'vue'; 
import { useRouter } from 'vue-router';

export default {
  name: "BrandSection",
  components: {
    mainbutton,
    seconbutton
  },
  setup(){
    // state
    const promotionStore = usePromotionStore();
    const router = useRouter();

    // lifecycle
    onMounted(() => {
      promotionStore.fetchCurrentFlashSale();
    })

    return {
      router,
      promotionStore
    }
  }
}
</script>

<style scoped>
.brand-section {
  background: linear-gradient(135deg, rgba(255, 245, 245, 0.8) 0%, rgba(255, 250, 240, 0.8) 100%);
  padding: 2rem 1rem;
  border-radius: 12px;
  margin-top: 1rem;
}

.brand-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.text-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.5rem;
}

.text-content h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  line-height: 1.4;
  margin: 0;
}

.discount-info {
  font-size: 1rem;
  color: #555;
  background-color: rgba(255, 224, 178, 0.5);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px dashed #ffb74d;
}

.discount-info .highlight {
  font-weight: 700;
  color: #ef6c00;
}

.btn__section {
  display: flex;
  gap: 1rem;
  width: 100%;
  justify-content: center;
  flex-wrap: wrap;
}

.image-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-content img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Tablet */
@media (min-width: 768px) {
  .brand-section {
    padding: 3rem 2rem;
    margin: 2rem;
  }
  
  .text-content h2 {
    font-size: 2rem;
  }
  
  .btn__section {
    width: 100%;
    flex-wrap: nowrap;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .brand-content {
    flex-direction: row;
    justify-content: space-between;
    text-align: left;
  }
  
  .text-content {
    align-items: flex-start;
    text-align: left;
    flex: 1;
  }
  
  .btn__section {
    justify-content: flex-start;
  }
  
  .image-content {
    flex: 1;
    justify-content: flex-end;
  }
  
  .image-content img {
    max-width: 90%;
  }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .brand-section {
    padding: 4rem 3rem;
  }
  
  .text-content h2 {
    font-size: 2.5rem;
  }
}
</style>