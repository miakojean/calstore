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
    // On change le type pour accepter un objet d'erreurs venant de Django
    const error = ref<any>(null); 

    const cartStore = useCartStore();
    const currentCartId = computed(() => (cartStore.cartUnormaled as any).id || null);

    const checkoutData = ref<Checkout>({
        cart_id: currentCartId.value,
        shipping_address: '',
        billing_address: '',
        fullName: '',
        phone_number: '',
        email: '',
        payment_method: 'A la livraison',
        agree_terms: true
    }); 

    // checkoutStore.ts
    const initiateCheckout = async () => {
        error.value = null; // Reset les erreurs précédentes

        // --- VALIDATION LOCALE (Tuer l'envoi dans l'œuf) ---
        const localErrors: any = {};

        if (!checkoutData.value.fullName?.trim()) localErrors.fullName = "Le nom est obligatoire.";
        if (!checkoutData.value.email?.trim()) localErrors.email = "L'email est obligatoire.";
        if (!checkoutData.value.phone_number?.trim()) localErrors.phone_number = "Le téléphone est obligatoire.";
        if (!checkoutData.value.shipping_address?.trim()) localErrors.shipping_address = "L'adresse de livraison est requise.";

        // Si on a des erreurs locales, on arrête TOUT ici
        if (Object.keys(localErrors).length > 0) {
            error.value = localErrors;
            return false; // La requête ne sera jamais lancée
        }

        // --- ENVOI REQUÊTE (Si valide) ---
        isLoading.value = true;
        checkoutData.value.cart_id = currentCartId.value;

        try {
            await api.post('ecommerce/checkout/', checkoutData.value);
            await cartStore.clearCart();
            return true; 
        } catch (err: any) {
            // Erreurs venant de Django (ex: email déjà utilisé, stock épuisé)
            error.value = err.response?.data || "Une erreur serveur est survenue";
            return false; 
        } finally {
            isLoading.value = false;
        }
    }

    return { isLoading, checkoutData, error, initiateCheckout, cartStore }
});

export {useCheckoutStore}