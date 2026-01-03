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

const useCategoryStore = defineStore('category', () => {
    
    // State - Données des catégories
    const currentCategory = ref<Category | null>(null);
    const categories = ref<Category[]>([]);
    
    // CHANGEZ CECI : stocker les produits par catégorie
    const categoryProducts = ref<Record<string, Product[]>>({}); // { 'chaussures': [...], 'sac_a_mains': [...] }
    
    // CHANGEZ CECI : stocker le loading par catégorie
    const loadingStates = ref<Record<string, boolean>>({});
    
    const error = ref<string | null>(null);

    // Computed
    const totalCategories = computed(() => categories.value.length);
    
    // Nouveau computed pour récupérer les produits d'une catégorie spécifique
    const getProductsBySlug = (slug: string) => {
        return computed(() => categoryProducts.value[slug] || []);
    };
    
    const isLoadingForSlug = (slug: string) => {
        return computed(() => loadingStates.value[slug] || false);
    };

    // Actions
    const fetchCategoryWithProducts = async (categorySlug: string) => {
        // Réinitialiser le loading pour cette catégorie
        loadingStates.value[categorySlug] = true;
        error.value = null;
        
        try {
            const response = await api.get(`/ecommerce/category-products/${categorySlug}`);
            
            if (response.data && response.data.status === 'success') {
                // Stocker les produits par catégorie
                categoryProducts.value[categorySlug] = response.data.products || [];
                
                console.log(`✅ Produits récupérés pour ${categorySlug}:`, categoryProducts.value[categorySlug]);
            } else {
                error.value = response.data?.message || 'Erreur inconnue';
                console.error(`❌ Erreur API pour ${categorySlug}:`, response.data);
            }
        } catch (err: any) {
            console.error(`❌ Erreur pour ${categorySlug}:`, err);
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
        } finally {
            loadingStates.value[categorySlug] = false;
        }
    }

    const fetchAllCategories = async () => {
        // Garder un loading global pour toutes les catégories
        loadingStates.value['all'] = true;
        error.value = null;
        
        try {
            const response = await api.get('/ecommerce/category-list');
            
            if (response.data && response.data.status === 'success') {
                categories.value = response.data.data || [];
                console.log("✅ Toutes les catégories récupérées :", categories.value);
            } else {
                error.value = response.data?.message || 'Erreur inconnue';
            }
        } catch (err: any) {
            console.error("❌ Erreur lors de la récupération des catégories :", err);
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
        } finally {
            loadingStates.value['all'] = false;
        }
    }

    // Réinitialiser l'état pour une catégorie spécifique
    const resetCategory = (slug: string) => {
        delete categoryProducts.value[slug];
        delete loadingStates.value[slug];
    }

    // Récupérer un produit par son ID et sa catégorie
    const getProductById = (categorySlug: string, productId: number | string): Product | undefined => {
        const products = categoryProducts.value[categorySlug];
        if (!products) return undefined;
        return products.find(product => product.id === productId);
    }

    return {
        // State
        currentCategory,
        categories,
        categoryProducts, // Garder pour compatibilité
        loadingStates,
        error,
        
        // Computed
        totalCategories,
        getProductsBySlug,
        isLoadingForSlug,
        
        // Actions
        fetchCategoryWithProducts,
        fetchAllCategories,
        resetCategory,
        getProductById
    };
});

export { useCategoryStore };