<template>
  <form @submit.prevent="makeCheckout" class="flex flex-col gap-2">
    <inputfamily 
      label="Nom complet" 
      v-model="checkoutStore.checkoutData.fullName" 
      name="fullName" 
      placeholder="Entrez votre nom complet" 
    />
    <inputfamily 
      label="Numéro de téléphone" 
      v-model="checkoutStore.checkoutData.phone_number" 
      name="phone" 
      placeholder="Entrez votre numéro de téléphone" 
    />
    <inputfamily 
      label="Adresse e-mail" 
      v-model="checkoutStore.checkoutData.email" 
      name="email" 
      placeholder="Entrez votre adresse e-mail" 
      type="email"
    />
    <inputfamily 
      label="Adresse de livraison" 
      v-model="checkoutStore.checkoutData.shipping_address" 
      name="shippingAddress" 
      placeholder="Entrez votre adresse de livraison"
    />
    <checkoutButton 
      label="Payer maintenant" 
      :isLoading="checkoutStore.isLoading" 
      @handleClicked="makeCheckout" 
    />
  </form>
</template>

<script lang="ts">
import { useCheckoutStore } from '../../stores/checkoutStore';
import { useCartStore } from '../../stores/cartStore'; // Importez aussi le cartStore
import inputfamily from '../input/inputfamily.vue';
import checkoutButton from '../button/checkoutButton.vue';
export default {
  components: {
    inputfamily,
    checkoutButton
  },
  setup() {
    const checkoutStore = useCheckoutStore();
    const cartStore = useCartStore();

    const makeCheckout = async () => {
  
      
      // 2. Debug pour voir les données
      console.log("Données envoyées :", checkoutStore.checkoutData);
      
      // 3. Lancer la commande
      await checkoutStore.initiateCheckout();
    };

    return { checkoutStore, cartStore, makeCheckout };
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
</style>