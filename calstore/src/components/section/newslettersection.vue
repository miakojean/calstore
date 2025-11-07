<template>
    <section>

        <h4>S'abonner à la newsletter</h4>

        <div class="newsletter__form">
            <inputfamily/>
            <mainbutton label="s'abonner"/>
        </div>

    </section>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import mainbutton from '../button/mainbutton.vue';
import inputfamily from '@/input/inputfamily.vue';

export default {
    name: 'CategorySection',
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


        // Return everything that should be available in template
        return {
            
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