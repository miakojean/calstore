<template>
    <section class="checkout-section">
        <div class="checkout-form-container">
            <checkoutForm />
        </div>
        <div class="cart-summary-container">
            <cartSection />
        </div>
    </section>
</template>

<script lang="ts">
import checkoutForm from '../forms/checkoutForm.vue';
import cartSection from './cartSection.vue';

export default {
    name: "CheckoutSection",
    components: {
        checkoutForm,
        cartSection
    }
}
</script>

<style scoped>
.checkout-section {
    display: flex;
    width: 100%;
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
    gap: 30px;
}

.checkout-form-container,
.cart-summary-container {
    flex: 1;
    min-width: 0; /* Important pour éviter l'overflow */
}

/* Pour les écrans plus petits, passez en colonne */
@media (max-width: 1024px) {
    .checkout-section {
        flex-direction: column;
    }
    
    .checkout-form-container,
    .cart-summary-container {
        width: 100%;
    }
}
</style>