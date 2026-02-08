import { defineStore } from "pinia";
import { ref, computed } from 'vue'
import api from "@/_services/api";

// Interfaces exportées
export interface Category {
    id: number | string;
    name: string;
    slug: string;
    description?: string;
    image?: string;
    image_url?: string;
    parentId?: number | string;
    productCount?: number;
    is_active?: boolean;
}

export interface Product {
    id: number | string;
    name: string;
    slug: string;
    short_description?: string;
    description: string;
    price: number;
    compare_price?: number;
    quantity: number;
    is_active: boolean;
    is_featured: boolean;
    is_on_sale: boolean;
    discount_percentage: number;
    in_stock: boolean;
    main_image_url?: string;
    images?: any[];
    variants?: any[];
    category: string;
    brand?: any;
}

export const useCategoryStore = defineStore('category', () => {

    // --- CONFIGURATION DU CACHE ---
    const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes en millisecondes
    const lastFetched = ref<Record<string, number>>({});

    // --- STATE ---
    const categories = ref<Category[]>([]);
    const categoryProducts = ref<Record<string, Product[]>>({});
    const loadingStates = ref<Record<string, boolean>>({});
    const error = ref<string | null>(null);

    // --- UTILS ---
    const isCacheValid = (key: string) => {
        const lastUpdate = lastFetched.value[key];
        if (!lastUpdate) return false;
        return (Date.now() - lastUpdate) < CACHE_DURATION;
    };

    // --- ACTIONS ---

    /**
     * Récupère les produits d'une catégorie avec gestion du cache
     */
    const fetchCategoryWithProducts = async (categorySlug: string, force = false) => {
        // Si le cache est valide et qu'on ne force pas, on arrête ici
        if (!force && isCacheValid(`products_${categorySlug}`) && categoryProducts.value[categorySlug]) {
            console.log(`[Cache] Utilisation des données locales pour : ${categorySlug}`);
            return;
        }

        loadingStates.value[categorySlug] = true;
        error.value = null;
        
        try {
            const response = await api.get(`/ecommerce/category-products/${categorySlug}`);
            
            if (response.data && response.data.status === 'success') {
                categoryProducts.value[categorySlug] = response.data.products || [];
                // Mise à jour du timestamp du cache
                lastFetched.value[`products_${categorySlug}`] = Date.now();
            } else {
                error.value = response.data?.message || 'Erreur inconnue';
            }
        } catch (err: any) {
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
        } finally {
            loadingStates.value[categorySlug] = false;
        }
    }

    /**
     * Récupère la liste de toutes les catégories avec gestion du cache
     */
    const fetchAllCategories = async (force = false) => {
        if (!force && isCacheValid('all_categories') && categories.value.length > 0) {
            console.log("[Cache] Liste des catégories déjà à jour");
            return;
        }

        loadingStates.value['all'] = true;
        
        try {
            const response = await api.get('/ecommerce/category-list');
            if (response.data && response.data.status === 'success') {
                categories.value = response.data.data || [];
                lastFetched.value['all_categories'] = Date.now();
            }
        } catch (err: any) {
            error.value = "Erreur lors de la récupération des catégories";
        } finally {
            loadingStates.value['all'] = false;
        }
    }

    const resetCategory = (slug: string) => {
        delete categoryProducts.value[slug];
        delete loadingStates.value[slug];
        delete lastFetched.value[`products_${slug}`];
    }

    return {
        categories,
        categoryProducts,
        loadingStates,
        error,
        fetchAllCategories,
        fetchCategoryWithProducts,
        resetCategory,
        // Getters
        totalCategories: computed(() => categories.value.length),
        getProductsBySlug: (slug: string) => computed(() => categoryProducts.value[slug] || []),
        isLoadingForSlug: (slug: string) => computed(() => loadingStates.value[slug] || false)
    };
});