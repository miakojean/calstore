<template>
    <section class="grid grid-cols-2 gap-4 h-screen">
        <div class="image-content">
            <img 
                src="../../assets/images/Copilot_20251112_142208.png" 
                alt=""
                class=""
            >
        </div>
        <div class="flex flex-col gap-4 items-center justify-center">
            <h2>Qui sommes-nous?</h2>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. 
                Ipsum distinctio voluptatibus doloremque? 
                Quod inventore itaque esse rerum, 
                voluptas minus tenetur impedit, 
                debitis, laboriosam ut temporibus? 
                Porro rem ex totam quia.
            </p>
        </div>
    </section>
</template>

<script>
export default {

}
</script>

<style scoped>
.image-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-content img {
  width: 100%;
  height: 100%;
  max-width: 500px;
  max-height: 500px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>