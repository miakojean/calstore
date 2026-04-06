<template>
    <section class="grid grid-cols-1 gap-4 h-screen md:grid-cols-2">
        <div class="image-content">
            <img 
                src="../../assets/images/Copilot_20251112_142208.png" 
                alt=""
                class=""
            >
        </div>
        <div class="flex flex-col gap-4 justify-center items-center">
            <h2 class="">Qui sommes-nous?</h2>
            <p class="about-us-paragraph">
                Calstore est une boutique en ligne qui a pour but de fournir des articles
                de meilleurs qualités aux meilleurs prix. Le rapport qualités prix défi tous
                nos concurents.
            </p>
            <p class="about-us-paragraph">
                Par ailleurs, notre service après vente est là pour vous assister et vous 
                faire passer un très bon quart d'heure durant l'achat de votre de 
                votre article.
            </p>
            <div class="flex w-full justify-items-start">
                <mainbutton label="revenir à l'accueil"/>
            </div>
        </div>
    </section>
</template>

<script>
import mainbutton from '../button/mainbutton.vue';
export default {
    components:{
        mainbutton
    }
}
</script>

<style scoped>
.image-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-content img {
  width: 100%;
  height: 100%;
  max-width: 500px;
  max-height: 500px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2, .about-us-paragraph{
    width: 100%;
    text-align: start;
}
</style>