<template>
  <nav class="category__nav">
    <ul>
      <li 
        v-for="(category, index) in categories" 
        :key="index"
        :class="{ active: activeCategory === index }"
        @click="setActiveCategory(index)"
      >
        <span class="nav-text">{{ category }}</span>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'CategoryNav',
  data() {
    return {
      categories: ['Chaussures', 't-shirt', 'Chemises', 'Sac à main', 'Electroniques', 'Menages', 'Soins de beauté'],
      activeCategory: 0, // Premier élément actif par défaut
    }
  },
  methods: {
    setActiveCategory(index) {
      this.activeCategory = index;
      console.log(index)
    },
  }
}
</script>

<style scoped>
.category__nav {
  width: 100%;
  overflow-x: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

ul {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  list-style: none;
  margin: 0;
}

li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  position: relative;
  white-space: nowrap;
}

.nav-text {
  font-weight: 400;
  transition: all 0.3s ease;
  display: block; /* Important pour éviter les décalages */
}

/* Style au survol */
li:hover .nav-text {
  font-weight: 500;
}

/* Soulignement au survol */
li:hover::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #000;
  animation: underline 0.3s ease;
}

/* Style actif */
li.active .nav-text {
  font-weight: 700;
}

/* Soulignement pour l'élément actif */
li.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #000;
}

/* Animation pour le soulignement */
@keyframes underline {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  ul {
    gap: 1rem;
    padding: 0.5rem;
  }
  
  li {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
}
</style>