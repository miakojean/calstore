<template>
    <section class="checkout-section">
        <div class="checkout-form-container" v-if="!isSuccess">
            <checkoutForm @checkout-initiated="handleCheckoutInitiated"/>
        </div>
        <div class="cart-summary-container" v-if="!isSuccess">
            <cartSection />
        </div>

        <div class="checkout-succes-section" v-if="isSuccess">
            <successOrder />
        </div>
    </section>
</template>

<script lang="ts">
import checkoutForm from '../forms/checkoutForm.vue';
import cartSection from './cartSection.vue';
import successOrder from '../card/successOrder.vue';
import { ref } from 'vue';

export default {
    name: "CheckoutSection",
    components: {
        checkoutForm,
        cartSection,
        successOrder
    },
    setup() {
        const isSuccess = ref<boolean>(false);

        const handleCheckoutInitiated = (): void => {
            isSuccess.value = true;
        };

        return {
            isSuccess,
            handleCheckoutInitiated
        }
    },
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
.cart-summary-container,
.checkout-succes-section {
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