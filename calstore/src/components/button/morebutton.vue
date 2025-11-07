<template>
    <button>
        {{ label }}
        <span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
            </svg>
        </span>
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
    max-width: 300px;
    border: 1px solid var(--my-black-color);
    color: var(--my-black-color);
    padding: 0.7rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

</style>