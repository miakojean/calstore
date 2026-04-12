<template>
  <transition name="slide-up">
    <div 
      v-if="showBanner" 
      class="cookie-banner"
    >
      <p class="cookie-text">
        Nous utilisons des cookies pour améliorer votre expérience. 
        Voulez-vous les accepter ?
      </p>
      <div class="cookie-actions">
        <seconbutton label="Refuser" @click="handleReject" />
        <mainbutton label="Accepter" @click="handleAccept" />
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { ref, onMounted, computed } from "vue";
import mainbutton from "../button/mainbutton.vue";
import seconbutton from "../button/seconbutton.vue";
import { useCookieStore } from "@/stores/cookieStore";

export default {
  name: 'CookieToast',
  components: {
    mainbutton,
    seconbutton
  },
  setup() {
    const cookieStore = useCookieStore();

    // La bannière est visible uniquement si l'utilisateur n'a pas encore donné son consentement
    const showBanner = computed(() => !cookieStore.consentGiven);

    const handleAccept = () => {
      cookieStore.setCookieConsent(true);
    };

    const handleReject = () => {
      cookieStore.setCookieConsent(false);
    };

    // Pas besoin de onMounted pour lire le consentement : le store le fait déjà à l'initialisation
    // Mais on peut ajouter une vérification supplémentaire si nécessaire
    onMounted(() => {
      // Optionnel : forcer la réactivité si besoin (mais le computed réagit déjà)
      // console.log('Consentement initial :', cookieStore.consentGiven.value);
    });

    return {
      cookieStore,
      showBanner,
      handleAccept,
      handleReject
    };
  }
};
</script>

<style scoped>
/* Ton style existant est très bien, je le conserve */
.cookie-banner {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  max-width: 300px;
  padding: 1rem;
  background: #fff;
  color: #333;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  font-size: 0.9rem;
  z-index: 1000;
  opacity: 0.95;
}
.cookie-text {
  margin-bottom: 0.75rem;
  line-height: 1.4;
}
.cookie-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(40px);
}
</style>