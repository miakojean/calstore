<template>
    <div class="input__family">
        <transition name="slide-fade">
            <p v-if="showError && errorMessage" class="error__message">{{ errorMessage }}</p>
        </transition>
        <input 
            type="email" 
            :class="{ 'input--error': showError }"
            placeholder="Entrer votre email"
            v-model="inputValue"
            @blur="handleBlur"
        >
    </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  props: {
    modelValue: {
      type: String,
      default: ""
    },
    showError: {
      type: Boolean,
      default: false
    },
    errorMessage: {
      type: String,
      default: ""
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const inputValue = ref(props.modelValue);
    const isTouched = ref(false);

    const validateEmail = () => {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(inputValue.value);
    };

    const handleBlur = () => {
      isTouched.value = true;
    };

    // Mise à jour du champ quand modelValue change
    watch(() => props.modelValue, (val) => {
      inputValue.value = val;
    });

    // Émission vers le parent quand l'utilisateur tape
    watch(inputValue, (val) => {
      emit('update:modelValue', val);
    });

    return {
      inputValue,
      validateEmail,
      handleBlur
    };
  }
}
</script>

<style scoped>
.input__family {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

input {
  width: 100%;
  border: 1px solid #dbdbdb;
  border-radius: 1rem;
  padding: 1rem;
  outline: none;
  transition: border 0.3s ease;
}

input:focus {
  border: 1px solid #010101;
}

.input--error {
  border: 1px solid red;
}

.error__message {
  color: red;
  margin: 0;
  font-size: 0.875rem;
}

/* Transition pour le message d'erreur */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

</style>