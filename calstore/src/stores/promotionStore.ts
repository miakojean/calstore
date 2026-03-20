import { defineStore } from "pinia";
import { ref } from 'vue';
import api from "@/_services/api";

/**
 * Interface pour les produits d'une vente flash
 * Basée sur la méthode get_products du FlashSaleSimpleSerializer
 */
export interface FlashSaleSimpleProduct {
    id: number;
    name: string;
    slug: string;
    original_price: string;
    flash_price: string;
    stock_limit: number | null;
    sold_quantity: number;
    image: string | null;
    in_stock: boolean;
}

/**
 * Interface pour la vente flash actuelle
 * Basée sur les Meta fields de FlashSaleSimpleSerializer
 */
export interface FlashSaleSimple {
    id: number;
    name: string;
    image: string;
    start_time: string;
    end_time: string;
    products: FlashSaleSimpleProduct[];
}

export const usePromotionStore = defineStore('promotion', () => {

    // --- STATE ---
    const currentFlashSale = ref<FlashSaleSimple | null>(null);
    const loading = ref(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---

    /**
     * Récupère la vente flash active via l'endpoint dédié
     */
    const fetchCurrentFlashSale = async () => {
        loading.value = true;
        error.value = null;
        
        try {
            // Appel à l'URL définie dans votre fichier urls.py
            const response = await api.get('/promotion/flash-sales/current/');

            // Extraction des données depuis l'objet de réponse standardisé de la vue
            if (response.data.status === 'success' && response.data.data) {
                currentFlashSale.value = response.data.data;
            } else {
                currentFlashSale.value = null;
                // Optionnel : gérer le cas 'info' (aucune promotion active)
                if (response.data.status === 'info') {
                    console.log(response.data.message);
                }
            }
        } catch (err) {
            error.value = 'Erreur lors du chargement de la vente flash.';
            console.error("Store Error:", err);
            currentFlashSale.value = null;
        } finally {
            loading.value = false;
        }
    };

    return {
        currentFlashSale,
        loading,
        error,
        fetchCurrentFlashSale
    };
});