<template>
    <div class="product-card">
        <div class="image-container">
            <!-- Afficher le badge de réduction si discount_percentage > 0 -->
            <span v-if="product.discount_percentage > 0" class="discount-badge">
                -{{ product.discount_percentage }}%
            </span>
            <!-- CORRECTION ICI : Utiliser images[0].image ou main_image_url -->
            <img 
                :src="product.main_image_url" 
                :alt="product.name" 
                class="product-image"
                @error="handleImageError"
            >
            <!-- Overlay pour desktop -->
            <div class="overlay">
                <button class="quick-view-btn" @click="showProductDetail">Détail du produit</button>
            </div>
        </div>

        <div class="product-info">
            <div class="product-details">
                <h4 class="product-name">{{ product.name }}</h4>
                <p class="product-description">{{ product.short_description }}</p>
            </div>

            <div class="product-footer flex flex-col gap-2">
                <div class="price-section">
                    <div class="price-group">
                        <span class="current-price">{{ formatPrice(product.price) }}</span>
                        <!-- Afficher le prix comparé si disponible -->
                        <span v-if="product.compare_price" class="original-price">
                            {{ formatPrice(product.compare_price) }}
                        </span>
                    </div>
                   
                    <details-buton @click="addToCart" :is-loading="isLoading"/>
                </div>
                <addtocartbutton @click="proceedToCheckout" label="Ajouter au panier"/>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import detailsButon from '../button/detailsButon.vue';
import addtocartbutton from '../button/addtocartbutton.vue';
import type { Product } from '../../stores/categoryStore';
import { useRouter } from 'vue-router';

const props = defineProps<{
    product: Product;
    isLoading?: boolean;
}>();

const emit = defineEmits<{
    'add-to-cart': [product: Product];
    'show-product-detail': [product: Product];
}>();

const router = useRouter();

// Méthodes
const addToCart = () => {
    emit('add-to-cart', props.product);
};

const showProductDetail = () => {
    emit('show-product-detail', props.product);
};

const getStars = (rating: number) => {
    const fullStars = '★'.repeat(Math.floor(rating));
    const emptyStars = '☆'.repeat(5 - Math.floor(rating));
    return fullStars + emptyStars;
};

// Formater le prix
const formatPrice = (price: string | number): string => {
    if (!price) return '0,00 €';
    
    const numPrice = typeof price === 'string' ? parseFloat(price) : price;
    
    // Format français : 15 000,00 €
    return numPrice.toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }) + ' FCFA';
};

// Gérer les erreurs d'image
const handleImageError = (event: Event) => {
    const img = event.target as HTMLImageElement;
    img.src = '/images/placeholder-product.jpg';
};

const proceedToCheckout = () => {
    addToCart();
    router.push('/cart-checkout');
};

// Valeurs par défaut pour les props
const defaultProduct: Product = {
    id: 1,
    name: "Basket simple blanche",
    price: 89.99,
    images: [],
    short_description: "Description courte",
    description: "Description complète",
    discount_percentage: 0,
    compare_price: null,
};

// Appliquer les valeurs par défaut si nécessaire
const productWithDefaults = {
    ...defaultProduct,
    ...props.product
};
</script>

<style scoped>
/* VOTRE STYLE EXISTANT - inchangé */
.product-card {
    background: white;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #f0f0f0;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    position: relative;
    overflow: hidden;
    width: 100%;
    min-width: 300px;
    animation: fadeIn 0.5s ease;
    padding: 0.75rem;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.image-container {
    position: relative;
    border-radius: 0.75rem;
    overflow: hidden;
    background: #f8f9fa;
    aspect-ratio: 4/3;
}

.discount-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background-color: var(--primary-color, #ef4444);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 600;
    z-index: 10;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.product-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.product-card:hover .product-image {
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

.product-card:hover .overlay {
    opacity: 1;
}

.quick-view-btn {
    background: white;
    color: #333;
    border: none;
    padding: 0.5rem 0.75rem;
    border-radius: 2rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.75rem;
}

.quick-view-btn:hover {
    background: #000;
    color: white;
    transform: scale(1.05);
}

.product-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
    width: 100%;
}

.product-name {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
    margin: 0;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.product-description {
    color: #666;
    font-size: 0.75rem;
    margin: 0;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.price-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
}

.price-group {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex-wrap: nowrap;
    width: 100%;
}

.current-price {
    font-size: 1.125rem;
    font-weight: 700;
    color: #000;
}

.original-price {
    font-size: 0.5rem;
    color: #888;
    text-decoration: line-through;
}

.discount {
    background: #ff4444;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 600;
}

.details-button-container {
    margin-top: 0.25rem;
}

.cart-icon {
    width: 1rem;
    height: 1rem;
}

/* Responsive Design */
@media (min-width: 425px) {
    .product-card {
        gap: 1rem;
    }
    
    .price-section {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
    
    .details-button-container {
        margin-top: 0;
        margin-left: 0.5rem;
    }
    
    .price-group {
        gap: 0.5rem;
    }
}

@media (min-width: 640px) {
    .product-card {
        gap: 1.25rem;
    }
    
    .product-name {
        font-size: 1.125rem;
    }
    
    .product-description {
        font-size: 0.875rem;
    }
    
    .current-price {
        font-size: 1.25rem;
    }
    
    .original-price {
        font-size: 1rem;
    }
    
    
    .quick-view-btn {
        padding: 0.75rem 1.5rem;
        font-size: 0.875rem;
    }
    
    .overlay {
        display: flex;
    }
}

@media (min-width: 768px) {
    .product-card {
        padding: 0.5rem;
    }
    
    .details-button-container {
        margin-left: 1rem;
    }
}

@media (min-width: 1024px) {
    .product-card {
        padding: 0.5rem;
        max-width: 300px;
        min-width: 320px;
    }
    
    .product-name {
        font-size: 1.25rem;
    }
    
    .cart-icon {
        width: 1.25rem;
        height: 1.25rem;
    }
}

/* Masquer l'overlay sur mobile */
@media (max-width: 639px) {
    .overlay {
        display: none;
    }
}

/* Animation */
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

/* Très petits écrans */
@media (max-width: 374px) {
    .product-card {
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .current-price {
        font-size: 1rem;
    }
    
    .original-price {
        font-size: 0.75rem;
    }
    
    .add-to-cart-btn {
        padding: 0.5rem 0.75rem;
        font-size: 0.7rem;
    }
}
</style>