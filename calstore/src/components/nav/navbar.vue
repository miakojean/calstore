<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="logo">
        <h3>Calstore</h3>
    </div>

    <researchinput/>

    <!-- 
      <ul class="nav__links">
        <li>Accueil</li>
        <li>Produits</li>
        <li>Catégorie</li>
      </ul>
    -->

    <div class="btn__container">
      <cartButton/>
      <button class="btn">Connexion</button>
    </div>
  </nav>
</template>

<script>
import cartButton from '../button/cartButton.vue'
import researchinput from '@/input/researchinput.vue';
import Researchinput from '../../input/researchinput.vue';
export default {
  name: 'Navbar',
  components:{
    cartButton,
    researchinput,
    Researchinput,
  },
  data() {
    return {
      isScrolled: false
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 10
    }
  }
}
</script>

<style scoped>
.navbar{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-around;
    position: fixed; /* ou sticky selon vos besoins */
    top: 0;
    left: 0;
    z-index: 1000;
    background-color: white; /* Assurez-vous d'avoir un fond */
    transition: box-shadow 0.3s ease; /* Transition douce */
}

.navbar.scrolled {
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Léger shadow en bas */
}

.logo h3{
    font-size: 1.5rem;
    font-weight: 500;
}

.nav__links{
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.btn__container{
  display:flex;
  align-items: center;
  justify-content: space-around;
  gap: 0.5rem;
}
</style>