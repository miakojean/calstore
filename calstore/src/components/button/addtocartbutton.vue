<template>
    <button  
        class="add-to-cart-btn"
        @click="addToCart"
    >
        <span class="btn-icon" v-if="isLoading===false">🛒</span>
        <span v-if="isLoading===false">Ajouter au panier</span>

        <span v-else class="loading loading-spinner loading-md"></span>
    </button>
</template>

<script lang="ts">
import { ref } from 'vue';
export default {

    props:{
        isLoading:{
            type: Boolean,
            default: false
        }
    },

    emits:["handleAddToCart"],

    setup(props:object,{emit}){
        const addToCart = (article:object)=>{
            setTimeout(()=>{
                emit("handleAddToCart");
                console.log("Evènement émis");
            })
        }

        return{
            addToCart
        }
    }

}
</script>

<style scoped>

.add-to-cart-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.6rem ;
    border-radius: 0.8rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.add-to-cart-btn span{
    font-weight: 600;
}

.add-to-cart-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-icon {
    font-size: 1.1rem;
}

</style>