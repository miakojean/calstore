<template>
    <section>
        <h4>S'abonner à la newsletter</h4>

        <div class="newsletter__form">
            <inputfamily 
                v-model="payload.email" 
                ref="inputRef"
                :show-error="showEmailError"
                :errorMessage="errorMessage"
            />
            <mainbutton 
                label="s'abonner" 
                :isLoading="isLoading"
                @click="simulateapi"
            />
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue'
import mainbutton from '../button/mainbutton.vue';
import inputfamily from '../input/inputfamily.vue';

export default {
    name: 'NewsletterSection',
    components: {
        mainbutton,
        inputfamily
    },
    props: {
        title: {
            type: String,
            default: "S'abonner à la newsletter"
        }
    },
    setup(props) {
        const isLoading = ref(false)
        const inputRef = ref(null);
        const showEmailError = ref(false);
        const errorMessage = ref("")

        const payload = ref({
            email: ""
        });

        const simulateapi = () => {
            errorMessage.value = ""
            const isValid = inputRef.value?.validateEmail();
            showEmailError.value = !isValid;

            if (!isValid) {
                errorMessage.value = "Veuillez entrer une addresse valide";
                setTimeout(()=>{
                    errorMessage.value = ""
                }, 5000)
                return;
            }

            isLoading.value = true;

            setTimeout(() => {
                alert("Abonnement réussi !!!");
                isLoading.value = false;
                payload.value.email = ""; // Réinitialiser le champ
                showEmailError.value = false; // Réinitialiser l'erreur
            }, 1000);
        };

        return {
            inputRef,
            isLoading,
            errorMessage,
            showEmailError,
            simulateapi,
            payload
        }
    }
}
</script>

<style scoped>
.newsletter__form{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 0.5rem;
}
</style>