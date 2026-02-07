import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/_services/api";

const useQueryStore = defineStore('product-query', ()=>{

    // state
    const isLoading = ref<boolean>(false);
    const error = ref<string>('')
    const results = ref([]);

    // actions
    const makeProductQuery = async (q:string) => {

        isLoading.value = true,
        error.value = ''

        try {
            const response = await api.get(`ecommerce/products-query/?name=${q}`);
            
            if (response.data){
                results.value = response.data;
                isLoading.value = false;

                // debogage
                console.log('articles récupérés', results.value);

            } else {
                error.value = response.data?.message || 'Erreur inconnue';
                isLoading.value = false;
                console.error(`Erreur lors de la recup`);
            }
        }   catch(err:any){
            console.error(err);
            isLoading.value = false;
        }

    }

    return{
        // state
        isLoading,
        error,
        results,

        // actions
        makeProductQuery
    }


})

export {useQueryStore}