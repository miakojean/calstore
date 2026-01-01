import { defineStore } from "pinia";
import { ref, computed } from 'vue'
import api from "@/_services/api";

// Exportez l'interface pour qu'elle soit accessible
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
    const currentCategory = ref<Category | null>(null);  // Changé de nom pour éviter conflit
    const categories = ref<Category[]>([]);
    const categoryProducts = ref<Product[]>([]);  // Nouveau state pour les produits de la catégorie
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // Computed
    const totalCategories = computed(() => categories.value.length);
    const totalProductsInCategory = computed(() => categoryProducts.value.length);

    // Actions
    const fetchCategoryWithProducts = async (categorySlug: string) => {  // Renommé le paramètre
        isLoading.value = true;
        error.value = null;
        
        try {
            const response = await api.get(`/ecommerce/category-products/${categorySlug}`);
            
            if (response.data && response.data.status === 'success') {
                
                currentCategory.value = response.data.category_data;
                categoryProducts.value = response.data.products;
                
                console.log("Catégorie récupérée :", currentCategory.value);
                console.log("Produits récupérés :", categoryProducts.value);
            } else {
                error.value = response.data?.message || 'Erreur inconnue';
            }
        } catch (err: any) {
            console.error("Erreur lors de la récupération de la catégorie :", err);
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
        } finally {
            isLoading.value = false;
        }
    }

    // Si vous voulez aussi récupérer toutes les catégories
    const fetchAllCategories = async () => {
        isLoading.value = true;
        error.value = null;
        
        try {
            const response = await api.get('/ecommerce/category-list');
            
            if (response.data && response.data.status === 'success') {
                // Votre API retourne :
                // {
                //   status: 'success',
                //   message: '...',
                //   count: X,
                //   data: [...]  // <- Liste des catégories
                // }
                
                categories.value = response.data.data;
                console.log("Toutes les catégories récupérées :", categories.value);
            } else {
                error.value = response.data?.message || 'Erreur inconnue';
            }
        } catch (err: any) {
            console.error("Erreur lors de la récupération des catégories :", err);
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
        } finally {
            isLoading.value = false;
        }
    }

    // Réinitialiser l'état
    const resetCurrentCategory = () => {
        currentCategory.value = null;
        categoryProducts.value = [];
        error.value = null;
    }

    return {
        // State
        currentCategory,
        categories,
        categoryProducts,
        isLoading,
        error,
        
        // Computed
        totalCategories,
        totalProductsInCategory,
        
        // Actions
        fetchCategoryWithProducts,
        fetchAllCategories,
        resetCurrentCategory
    };
});

export { useCategoryStore };