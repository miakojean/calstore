// queryStore.ts
import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/_services/api";

const useQueryStore = defineStore('product-query', () => {
    // state
    const isLoading = ref<boolean>(false);
    const error = ref<string>('');
    const results = ref<any[]>([]);

    // actions

    const makeProductQuery = async (q: string) => {
        if (!q.trim()) {
            results.value = [];
            return;
        }

        isLoading.value = true;
        error.value = '';

        try {
            const response = await api.get(`ecommerce/products-query/`, {
                params: { name: q.trim() }
            });
            
            if (response.status === 200) {
                results.value = response.data.data || [];
                console.log('Articles récupérés:', results.value);
            } else {
                error.value = 'Erreur lors de la récupération des données';
                console.error('Erreur API:', response.status);
            }
        } catch (err: any) {
            error.value = err.response?.data?.message || 'Erreur réseau';
            console.error('Erreur:', err);
            results.value = [];
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // state
        isLoading,
        error,
        results,
        
        // actions
        makeProductQuery
    };
});

export { useQueryStore };