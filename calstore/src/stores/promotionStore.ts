import { defineStore } from "pinia";
import { ref } from 'vue'
import api from "@/_services/api";

// Interfaces exportées

export interface Flashsale {
    name: string;
    description: string;
    products: number[]; // IDs des produits en promotion
    start_time: string; // ISO 8601
    end_time: string;   // ISO 8601
    image?: string;
}

export interface FlashSaleProduct {
    flash_sale: number|string; // ID de la promotion
    product: number|string;    // ID du produit
    flash_price: number;      // Prix promotionnel
    stock_limit?: number;     // Limite de stock pour la promotion
    sold_quantity?: number;  // Quantité déjà vendue dans le cadre de la promotion
}

export const usePrmotionStore = defineStore('promotion', ()=> {

    // --- STATE ---
    const flashsale = ref<Flashsale | null>(null);
    const flashsales = ref<Flashsale[]>([]);
    const flashSaleProducts = ref<FlashSaleProduct[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---
    const fetchFlashsales = async () => {
        loading.value = true;
        error.value = null;
        try {
            const response = await api.get('/promotion/flash-sales/');
            flashsales.value = response.data;
            flashsale.value = response.data.data && response.data.data.length > 0 ? response.data.data[0] : null;
            console.log('Promotions flash récupérées :', flashsales.value);
        } catch (err) {
            error.value = 'Erreur lors du chargement des promotions flash.';
        } finally {
            loading.value = false;
        }
    };

    return {
        flashsale,
        flashsales,
        flashSaleProducts,
        loading,
        error,
        fetchFlashsales
    }
})