<template>
  <button
    class="hamburger"
    :class="{ 'is-active': isActive }"
    @click="toggle"
    :aria-label="ariaLabel"
    :style="buttonStyle"
  >
    <span class="hamburger-line"></span>
    <span class="hamburger-line"></span>
    <span class="hamburger-line"></span>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props pour personnaliser le bouton
const props = defineProps({
  initialActive: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: '#000'
  },
  size: {
    type: Number,
    default: 24 // taille en pixels (largeur/hauteur)
  },
  thickness: {
    type: Number,
    default: 2 // épaisseur des barres
  },
  ariaLabel: {
    type: String,
    default: 'Menu'
  }
})

// État local
const isActive = ref(props.initialActive)

// Événement émis lors du clic
const emit = defineEmits(['toggle', 'update:active'])

// Style dynamique pour le bouton
const buttonStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  '--line-color': props.color,
  '--line-thickness': `${props.thickness}px`,
  '--line-width': `${props.size * 0.8}px`, // les barres sont un peu plus courtes que le bouton
  '--line-radius': `${props.thickness / 2}px`
}))

// Bascule l'état et émet les événements
const toggle = () => {
  isActive.value = !isActive.value
  emit('toggle', isActive.value)
  emit('update:active', isActive.value)
}
</script>

<style scoped>
.hamburger {
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 0;
  position: relative;
  outline: none;
}

.hamburger-line {
  display: block;
  width: var(--line-width);
  height: var(--line-thickness);
  background-color: var(--line-color);
  border-radius: var(--line-radius);
  transition: transform 0.3s ease-in-out, opacity 0.2s ease-in-out;
  transform-origin: center;
}

/* Animation : transformation en croix */
.hamburger.is-active .hamburger-line:nth-child(1) {
  transform: translateY(calc(var(--line-thickness) * 4)) rotate(45deg);
}

.hamburger.is-active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.hamburger.is-active .hamburger-line:nth-child(3) {
  transform: translateY(calc(var(--line-thickness) * -4)) rotate(-45deg);
}

@media (min-width: 780px) {
  .hamburger {
    display: none;
  }
}
</style>