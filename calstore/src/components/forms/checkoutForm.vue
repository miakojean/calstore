<template>
  <form @submit.prevent="makeCheckout" class="flex flex-col gap-2">
    <inputfamily 
      label="Nom complet" 
      v-model="checkoutStore.checkoutData.fullName" 
      :error="formatError(checkoutStore.error?.fullName)"
      required
    />
    
    <inputfamily 
      label="Numéro de téléphone" 
      v-model="checkoutStore.checkoutData.phone_number" 
      :error="formatError(checkoutStore.error?.phone_number)"
      required
    />
    
    <inputfamily 
      label="Adresse e-mail" 
      v-model="checkoutStore.checkoutData.email" 
      :error="formatError(checkoutStore.error?.email)"
      type="email"
      required
    />

    <inputfamily 
      label="Adresse de livraison" 
      v-model="checkoutStore.checkoutData.shipping_address" 
      :error="formatError(checkoutStore.error?.shipping_address)"
      required
    />

    <div v-if="typeof checkoutStore.error === 'string'" class="error-field">
      <p>{{ checkoutStore.error }}</p>
    </div>

    <checkoutButton 
      label="Payer maintenant" 
      :isLoading="checkoutStore.isLoading" 
    />
  </form>
</template>

<script lang="ts">
import { useCheckoutStore } from '../../stores/checkoutStore';
import { useCartStore } from '../../stores/cartStore';
import inputfamily from '../input/inputfamily.vue';
import checkoutButton from '../button/checkoutButton.vue';

export default {
  components: { inputfamily, checkoutButton },
  emits: ['checkoutInitiated'],
  setup(props, { emit }) {
    const checkoutStore = useCheckoutStore();

    // Utilitaire pour transformer les tableaux d'erreurs Django en String
    const formatError = (err: any) => {
      if (Array.isArray(err)) return err[0]; // Prend le premier message
      return err;
    };

    const makeCheckout = async () => {
      // initiateCheckout retourne désormais un booléen
      const isSuccess = await checkoutStore.initiateCheckout();

      if (isSuccess) {
        emit('checkoutInitiated'); // N'est appelé que si l'API répond 200/201
      }
    };

    return { checkoutStore, makeCheckout, formatError };
  }
}
</script>

<style scoped>
form{
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.error-field{
  padding: 1rem;
  border-radius: 1rem;
  color: red;
}
</style>