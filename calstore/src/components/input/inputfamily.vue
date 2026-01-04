<template>
  <div class="input__family">
    <div class="label-row">
      <label :for="identifiant">{{ label }}</label>
      <div v-if="$slots['header-action']" class="header-action">
        <slot name="header-action"></slot>
      </div>
    </div>

    <div class="input-wrapper" :class="{ 'has-error': hasError || error }">
      <input 
        :type="type" 
        :id="identifiant" 
        :placeholder="placeholder"
        :value="modelValue"
        @input="handleInput"
        @blur="validateField"
        class="styled-input"
      >
      <span v-if="$slots.icon" class="input-icon">
        <slot name="icon"></slot>
      </span>
    </div>

    <span v-if="hasError || error" class="error-message">
      {{ errorMessage || error }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'InputFamily',
  props: {
    identifiant: {
      type: String,
      default: "Username"
    },
    label: {
      type: String,
      default: "Username"
    },
    placeholder: {
      type: String,
      default: ""
    },
    modelValue: {
      type: String,
      default: ""
    },
    required: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: "text"
    },
    error: {
      type: String,
      default: ""
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      hasError: false,
      errorMessage: "Ce champ est obligatoire",
      isTouched: false
    }
  },
  methods: {
    handleInput(event) {
      const value = event.target.value;
      this.$emit('update:modelValue', value);
      
      if (this.isTouched) {
        this.validateField();
      }
    },
    
    validateField() {
      this.isTouched = true;
      
      if (this.required && !this.modelValue.trim()) {
        this.hasError = true;
        return false;
      } else {
        this.hasError = false;
        return true;
      }
    },
    
    validate() {
      return this.validateField();
    },
    
    resetValidation() {
      this.hasError = false;
      this.isTouched = false;
    }
  },
  
  watch: {
    modelValue(newValue) {
      if (this.isTouched) {
        this.validateField();
      }
    }
  }
}
</script>

<style scoped>
.input__family {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem; /* Espacement entre les champs */
}

/* --- Header du champ (Label + Action) --- */
.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6B7280; /* Gris moyen type Tailwind gray-500 */
}

.header-action {
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}

/* --- Wrapper Input (pour gérer l'icône absolue) --- */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.styled-input {
  width: 100%;
  padding: 0.85rem 1rem;
  padding-right: 2.8rem; /* Place pour l'icône à droite */
  font-size: 0.95rem;
  color: #1F2937; /* Texte presque noir */
  background-color: #ffffff;
  border: 1px solid #E5E7EB; /* Gris très clair */
  border-radius: 12px; /* Arrondi prononcé comme sur l'image */
  outline: none;
  transition: all 0.2s ease-in-out;
}

/* Placeholder styling */
.styled-input::placeholder {
  color: #9CA3AF;
  font-weight: 400;
}

/* Focus State - Bordure bleue */
.styled-input:focus {
  border-color: #3B82F6;
  box-shadow: 0 0 0 1px #3B82F6; /* Légère lueur bleue */
}

/* --- Gestion des Icônes --- */
.input-icon {
  position: absolute;
  right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none; /* L'icône ne bloque pas le clic */
  color: #9CA3AF; /* Couleur de l'icône par défaut */
}

/* --- Gestion des Erreurs --- */
.input-wrapper.has-error .styled-input {
  border-color: #EF4444; /* Rouge */
  background-color: #FEF2F2;
}

.input-wrapper.has-error .input-icon {
  color: #EF4444;
}

.error-message {
  color: #EF4444;
  font-size: 0.8rem;
  font-weight: 500;
  margin-top: -0.25rem;
}
</style>