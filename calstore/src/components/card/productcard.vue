<template>
    <div class="product__card">
        <img src="../../assets/pic/Copilot_20251107_112529.png" alt="">
        <p>Basket simple blanche</p>
    </div>
</template>

<script>
export default {

    props:{
        picRoute:{
            type:String,
            default:()=>{
                "../../assets/pic/Copilot_20251107_112529.png"
            }
        }
    }

}
</script>

<style scoped>
/* for mobile */
img{
    width:280px;
    height: 280px;
    background-size: cover;
    border-radius: 1rem;
}

.product__card{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

</style>