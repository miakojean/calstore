<template>
    <div class="product__card" :data-product-id="product.id">
        <div class="image__container">
            <img :src="'/pic/' + product.image" :alt="product.name" class="product-image">
            <div class="overlay">
                <button class="quick-view-btn">Voir plus</button>
            </div>
        </div>
        <div class="product-info">
            <p class="product-name">{{ product.name }}</p>
            <p class="product-description">{{ product.description }}</p>
            <div class="price-section">
                <span class="current-price">{{ product.price }} €</span>
                <span v-if="product.originalPrice" class="original-price">{{ product.originalPrice }} €</span>
                <span v-if="product.discount" class="discount">{{ product.discount }}</span>
            </div>
            <div v-if="product.rating" class="rating">
                <span class="stars">{{ getStars(product.rating) }}</span>
                <span class="review-count">({{ product.reviewCount }})</span>
            </div>
            <button class="add-to-cart-btn" @click="addToCart">
                <span class="btn-icon"> 
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                    </svg>
                </span>
                Ajouter au panier
            </button>
        </div>
    </div>
</template>

<script>
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
    methods: {
        addToCart() {
            this.$emit('add-to-cart', this.product)
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
.product__card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1rem;
    background: white;
    border-radius: 1.5rem;
    padding: 1.2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid #f0f0f0;
    position: relative;
    overflow: hidden;
}

.product__card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.image__container {
    position: relative;
    border-radius: 1rem;
    overflow: hidden;
    background: #f8f9fa;
}

.product-image {
    width: 100%;
    height: 220px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.product__card:hover .product-image {
    transform: scale(1.05);
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.product__card:hover .overlay {
    opacity: 1;
}

.quick-view-btn {
    background: white;
    color: #333;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 2rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.quick-view-btn:hover {
    background: #000;
    color: white;
    transform: scale(1.05);
}

.product-info {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.product-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
    margin: 0;
    line-height: 1.3;
}

.product-description {
    color: #666;
    font-size: 0.9rem;
    margin: 0;
}

.price-section {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.current-price {
    font-size: 1.3rem;
    font-weight: 700;
    color: #000;
}

.original-price {
    font-size: 1rem;
    color: #888;
    text-decoration: line-through;
}

.discount {
    background: #ff4444;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: 600;
}

.rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.stars {
    color: #ffc107;
    font-size: 1rem;
}

.review-count {
    color: #666;
    font-size: 0.9rem;
}

.add-to-cart-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 1.5rem;
    border-radius: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.add-to-cart-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-icon {
    font-size: 1.1rem;
}

/* Responsive */
@media (max-width: 768px) {
    .product__card {
        padding: 1rem;
        border-radius: 1.2rem;
    }
    
    .product-image {
        height: 200px;
    }
    
    .current-price {
        font-size: 1.2rem;
    }
    
    .add-to-cart-btn {
        padding: 0.8rem 1.2rem;
        font-size: 0.9rem;
    }
}

/* Animation pour le chargement */
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

.product__card {
    animation: fadeIn 0.5s ease;
}
</style>