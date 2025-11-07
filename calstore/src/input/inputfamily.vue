<template>
    <div class="input__family">
        <input type="email" placeholder="Entrer votre email">
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.input__family{
    width: 100%;
}

input{
    width: 100%;
    border: 1px solid #dbdbdb;
    border-radius: 1rem;
    padding: 1rem;
    outline: none;
}

input:focus{
    border: 1px solid #010101;
    outline: none;
}
</style>