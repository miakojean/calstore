<template>
    <div class="product-card bg-white rounded-2xl p-4 sm:p-5 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 ease-in-out transform hover:-translate-y-1 flex flex-col gap-4 relative overflow-hidden animate-fade-in">
        <div class="image-container relative rounded-xl overflow-hidden bg-gray-50">
            <img 
                :src="'/pic/' + product.image" 
                :alt="product.name" 
                class="product-image w-full h-48 sm:h-56 object-cover transition-transform duration-300 ease-in-out hover:scale-105"
            >
            <!-- Overlay pour desktop -->
            <div class="overlay absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 ease-in-out">
                <button class="quick-view-btn bg-white text-gray-800 px-6 py-3 rounded-full font-semibold hover:bg-black hover:text-white transform hover:scale-105 transition-all duration-300 ease-in-out">
                    Détail du produit
                </button>
            </div>
        </div>

        <div class="product-info flex flex-col gap-3 flex-1">
            <h3 class="product-name text-lg font-semibold text-gray-900 line-clamp-2 leading-tight">
                {{ product.name }}
            </h3>
            
            <p class="product-description text-sm text-gray-600 line-clamp-2">
                {{ product.description }}
            </p>

            <div class="price-section flex items-center justify-between gap-2 w-full">
                <div class="flex items-center gap-2 flex-wrap">
                    <span class="current-price text-xl font-bold text-gray-900">
                        {{ product.price }} €
                    </span>
                    <span v-if="product.originalPrice" class="original-price text-base text-gray-500 line-through">
                        {{ product.originalPrice }} €
                    </span>
                    <span v-if="product.discount" class="discount bg-red-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                        {{ product.discount }}
                    </span>
                </div>
                <details-buton/>
            </div>
            
            <button 
                @click="addToCart"
                class="add-to-cart-btn bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-4 py-4 rounded-xl font-semibold hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-300 ease-in-out flex items-center justify-center gap-2 mt-2"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                </svg>
                Ajouter au panier
            </button>
        </div>
    </div>
</template>

<script>
import detailsButon from '../button/detailsButon.vue';
export default {
    props: {
        product: {
            type: Object,
            required: true,
            default: () => ({
                id: 1,
                name: "Basket simple blanche",
                price: 89.99,
                image: "Copilot_20251107_112529.png",
                description: "Basket blanche élégante et confortable",
                originalPrice: null,
                discount: null,
                rating: null,
                reviewCount: null
            })
        }
    },

    components:{
        detailsButon,
    },
    methods: {
        addToCart() {
            this.$emit('add-to-cart', this.product)
        },
        showProductDetail() {
            this.$emit('show-detail', this.product)
        },
        getStars(rating) {
            const fullStars = '★'.repeat(Math.floor(rating));
            const emptyStars = '☆'.repeat(5 - Math.floor(rating));
            return fullStars + emptyStars;
        }
    }
}
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Masquer l'overlay sur mobile */
@media (max-width: 768px) {
    .overlay {
        display: none;
    }
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>