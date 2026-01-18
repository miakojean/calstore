import { defineStore } from "pinia";
import { ref, computed } from 'vue';
import api from "@/_services/api";
import { useCartStore } from "./cartStore";

// Interface exportée
// checkoutStore.ts
export interface Checkout {
    fullName?: string; // Ajouté pour correspondre à votre formulaire
    phone_number?: string;
    email?: string;
    cart_id?: string | null;
    shipping_address?: string;
    billing_address?: string;
    payment_method?: string;
    agree_terms?: boolean; // Requis par votre CheckoutSerializer Django
}

const useCheckoutStore = defineStore('checkout', () => {
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    const cartStore = useCartStore();
    
    // Initialisez checkoutData avec des valeurs par défaut

    const currentCartId = computed(() => {
        // Supposons que cartStore a une propriété cartId
        return (cartStore.cartUnormaled as any).id || null;
    });

    const checkoutData = ref<Checkout>({
        cart_id: currentCartId.value,
        shipping_address: '',
        billing_address: '',
        fullName: '',
        phone_number: '',
        email: '', // À dynamiser plus tard
        payment_method: 'A la livraison',
        agree_terms: true
    });

    const initiateCheckout = async () => {
        isLoading.value = true;
        checkoutData.value.cart_id = currentCartId.value; // On injecte l'ID du panier avant l'envoi

        try {
            // Note: Vérifiez l'URL, votre Serializer Django attend cart_id, email, shipping_address, etc.
            const response = await api.post('ecommerce/checkout/', checkoutData.value);
            console.log('Réponse du serveur:', response.data);
        } catch (err: any) {
            error.value = err.response?.data || 'Erreur serveur';
            console.error('Détails erreur:', error.value);
        } finally {
            isLoading.value = false;
        }
    }

    return { isLoading, checkoutData, error, initiateCheckout, cartStore }
});

export {useCheckoutStore}