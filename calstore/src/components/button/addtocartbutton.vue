<template>
    <button  
        class="add-to-cart-btn"
        @click="addToCart"
    >
        <span v-if="isLoading===false">Acheter</span>
        <span v-else class="loading loading-spinner loading-md"></span>
    </button>
</template>

<script lang="ts">
import { ref } from 'vue';
export default {

    name:'addtocartbutton',

    props:{
        isLoading:{
            type: Boolean,
            default: false
        },
        label:{
            type: String,
            default:''
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
    background-color: #ed5959;
    color: white;
    border: none; 
    padding: 0.8rem ;
    border-radius: 1.5rem;
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
    box-shadow: 0 4px 12px #db8585;
}

.btn-icon {
    font-size: 1.1rem;
}

</style>