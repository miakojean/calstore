<template>
    <div class="success__container">
        <h2>Commande effectuée</h2>
        <p>Nous vous contacterons dans les minutes qui suivent.</p>
        <div class="btn__actions">
            <mainbutton label="Retour à l'accueil" @click="goToIndex"/>
        </div>
    </div>
</template>

<script lang="ts">
import mainbutton from '../button/mainbutton.vue';
import seconbutton from '../button/seconbutton.vue';
import { useRouter } from 'vue-router';
export default {
    name: "successOrder",
    components: {
        mainbutton,
        seconbutton
    },
    setup(){
        const router = useRouter();
        const goToIndex = ()=>{
            router.push('/');
        }

        return{
            router,
            goToIndex
        }
    }
}
</script>

<style scoped>
.success__container{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 2rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    background-color: #f9fafb;
}

.btn__actions{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}
</style>