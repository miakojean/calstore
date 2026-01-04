<template>
  <form action="" class="flex flex-col gap-2">
    <inputfamily label="Nom complet" type="text" name="fullName" placeholder="Entrez votre nom complet" />
    <inputfamily label="Numéro de téléphone" type="tel" name="phone" placeholder="Entrez votre numéro de téléphone" />
    <mainbutton label="Finaliser la commande" />
  </form>
</template>

<script>
import inputfamily from '../input/inputfamily.vue';
import mainbutton from '../button/mainbutton.vue';
export default {
    components: {
        inputfamily,
        mainbutton
    }
}
</script>

<style scoped>
form{
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>