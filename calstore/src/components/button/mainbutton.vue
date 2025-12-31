<template>
  <button>
    <span v-if="isLoading === false">{{ label }}</span>
    <span
      v-if="isLoading === true"
      class="loading loading-spinner loading-md"
    >
    </span>
  </button>
</template>

<script lang="ts">
export default {
  props:{
    label:{
      type:String,
      default:"Commander"
    },
    isLoading:{
      type:Boolean,
      default: false
    }
  },
  emits:["handleClicked"],
  setup(props, {emit}){
    const voir = ()=>{
      emit("handleClicked")
      console.log("Vous avez émit un évènement")
    }

    return{
      voir
    }
  }
}
</script>

<style scoped>

/* for mobile */
button{
    width: 100%;
    max-width: 200px;
    background: var(--my-black-color);
    color: #fff;
    padding: 0.7rem;
    border-radius: 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
}

</style>