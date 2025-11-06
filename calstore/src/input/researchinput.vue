<template>
  <div class="input__family">
    <input type="text" placeholder="Trouver un produit">
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
input{
  background: var(--background-color);
  width: 100%;
  max-width: 500px;
  padding: 0.8rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
}

input:focus{
  outline: none;
}
</style>