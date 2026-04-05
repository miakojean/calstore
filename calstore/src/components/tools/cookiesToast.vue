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
        <seconbutton label="refuser" @click="rejectCookies"/>
        <mainbutton label="accepter" @click="acceptCookies"/>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { ref, onMounted } from "vue"
import mainbutton from "../button/mainbutton.vue"
import seconbutton from "../button/seconbutton.vue"

export default{
  name:'CookieToast',
  components:{
    mainbutton,
    seconbutton
  },
  setup(){
    const showBanner = ref(true)

    onMounted(() => {
      const consent = localStorage.getItem("cookie-consent")
      if (!consent) {
        showBanner.value = true
      }
    })

    function acceptCookies() {
      localStorage.setItem("cookie-consent", "accepted")
      showBanner.value = false
    }

    function rejectCookies() {
      localStorage.setItem("cookie-consent", "rejected")
      showBanner.value = false
    }

    return{
      showBanner,
      acceptCookies,
      rejectCookies
    }
  }
}
</script>

<style scoped>
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

/* Texte */
.cookie-text {
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

/* Boutons */
.cookie-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
.btn {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: transform 0.2s ease;
}
.btn:hover {
  transform: scale(1.05);
}
.btn.accept {
  background-color: var(--primary-color, #4CAF50);
  color: white;
}
.btn.reject {
  background-color: #ddd;
  color: #333;
}

/* Animation slide depuis le bas */
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