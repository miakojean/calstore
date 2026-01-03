import { defineStore } from "pinia";
import { ref, computed } from 'vue'
import api from "@/_services/api";

// Exportez l'interface pour qu'elle soit accessible
export interface CartItem {
  id: string | number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
  maxStock?: number;
}

const useCartStore = defineStore('cart', () => {
    const cart = ref<CartItem[]>([]);

    // Computed - Total d'articles dans le panier
    const totalItems = computed(() => {
        return cart.value.reduce((total, item) => total + item.quantity, 0);
    });

    // Computed - Prix total du panier
    const totalPrice = computed(() => {
        return cart.value.reduce((total, item) => total + (item.price * item.quantity), 0);
    });

    // Computed - Vérifie si le panier est vide
    const isEmpty = computed(() => cart.value.length === 0);

    // Ajouter un article au panier
    const addToCart = (item: Omit<CartItem, 'quantity'>) => {
        // Normaliser le prix au format number (au cas où caller enverrait une chaîne formatée)
        const normalizePrice = (p: any): number => {
            if (p === null || p === undefined) return 0;
            if (typeof p === 'number') return p;
            if (typeof p === 'string') {
                // Retirer tout sauf chiffres, point et signe
                const numeric = p.replace(/[^0-9.-]+/g, '');
                const parsed = parseFloat(numeric);
                return isNaN(parsed) ? 0 : parsed;
            }
            return 0;
        }

        const priceNum = normalizePrice(item.price as any);

        const existingItem = cart.value.find(cartItem => cartItem.id === item.id);
        
        if (existingItem) {
            // Si l'article existe déjà, augmenter la quantité
            if (existingItem.maxStock && existingItem.quantity >= existingItem.maxStock) {
                console.warn(`Stock limit reached for ${item.name}`);
                return;
            }
            existingItem.quantity += 1;
            // Mettre à jour le prix si besoin (assurer que c'est un nombre)
            existingItem.price = priceNum;
        } else {
            // Sinon, ajouter un nouvel article avec quantité 1
            cart.value.push({
                ...item,
                price: priceNum,
                quantity: 1
            });
        }
        console.debug('[cartStore] addToCart -> cart now:', cart.value)
        
        // Sauvegarder dans le localStorage (optionnel)
        saveToLocalStorage();
    };

    // Supprimer un article du panier
    const removeFromCart = (itemId: string | number) => {
        const itemIndex = cart.value.findIndex(item => item.id === itemId);
        if (itemIndex !== -1) {
            cart.value.splice(itemIndex, 1);
            saveToLocalStorage();
        }
    };

    // Modifier la quantité d'un article
    const updateQuantity = (itemId: string | number, newQuantity: number) => {
        const item = cart.value.find(cartItem => cartItem.id === itemId);
        
        if (item) {
            if (newQuantity <= 0) {
                removeFromCart(itemId);
            } else if (item.maxStock && newQuantity > item.maxStock) {
                item.quantity = item.maxStock;
            } else {
                item.quantity = newQuantity;
            }
            saveToLocalStorage();
        }
    };

    // Augmenter la quantité d'un article
    const increaseQuantity = (itemId: string | number) => {
        const item = cart.value.find(cartItem => cartItem.id === itemId);
        if (item) {
            if (item.maxStock && item.quantity >= item.maxStock) {
                console.warn('Cannot exceed max stock');
                return;
            }
            item.quantity += 1;
            saveToLocalStorage();
        }
    };

    // Diminuer la quantité d'un article
    const decreaseQuantity = (itemId: string | number) => {
        const item = cart.value.find(cartItem => cartItem.id === itemId);
        if (item) {
            if (item.quantity > 1) {
                item.quantity -= 1;
            } else {
                removeFromCart(itemId);
            }
            saveToLocalStorage();
        }
    };

    // Vider complètement le panier
    const clearCart = () => {
        cart.value = [];
        localStorage.removeItem('cart');
    };

    // Vérifier si un article est dans le panier
    const isInCart = (itemId: string | number) => {
        return cart.value.some(item => item.id === itemId);
    };

    // Obtenir la quantité d'un article spécifique
    const getItemQuantity = (itemId: string | number) => {
        const item = cart.value.find(cartItem => cartItem.id === itemId);
        return item ? item.quantity : 0;
    };

    // Sauvegarder dans le localStorage
    const saveToLocalStorage = () => {
        if (typeof window !== 'undefined') {
            localStorage.setItem('cart', JSON.stringify(cart.value));
        }
    };

    // Charger depuis le localStorage
    const loadFromLocalStorage = () => {
        if (typeof window !== 'undefined') {
            const savedCart = localStorage.getItem('cart');
            if (savedCart) {
                try {
                    const parsed = JSON.parse(savedCart);
                    // Normaliser chaque item (prix en number, quantité en number)
                    cart.value = (parsed || []).map((it: any) => ({
                        id: it.id,
                        name: it.name,
                        price: typeof it.price === 'number' ? it.price : parseFloat(String(it.price).replace(/[^0-9.-]+/g, '')) || 0,
                        quantity: typeof it.quantity === 'number' ? it.quantity : parseInt(it.quantity, 10) || 1,
                        image: it.image || it.main_image_url || null,
                        maxStock: it.maxStock || null
                    }));
                } catch (error) {
                    console.error('Error loading cart from localStorage:', error);
                    cart.value = [];
                }
            }
        }
    };

    // Initialiser le store en chargeant depuis le localStorage
    loadFromLocalStorage();

    return {
        // State
        cart,
        
        // Computed
        totalItems,
        totalPrice,
        isEmpty,
        
        // Actions
        addToCart,
        removeFromCart,
        updateQuantity,
        increaseQuantity,
        decreaseQuantity,
        clearCart,
        isInCart,
        getItemQuantity,
        loadFromLocalStorage
    };
});

export { useCartStore };