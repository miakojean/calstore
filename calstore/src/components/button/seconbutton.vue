<template>
    <button>
        {{ label }}
    </button>
</template>

<script lang="ts">
export default {
    props:{
        label:{
            type:String,
            default:"voir produits"
        }
    },
    emits:['clicked'],
    setup(props:object, {emit}) {
        const goto = () =>{
            emit("clicked");
            console.log("Vous avez emit un évènement !!!")
        }

        return{
            goto,
        }
    },

}
</script>

<style scoped>

/* for mobile */
button{
    width: 100%;
    max-width: 200px;
    border: 1px solid var(--my-black-color);
    color: var(--my-black-color);
    padding: 0.7rem;
    border-radius: 0.5rem;
    font-size: 1rem;
}

</style>