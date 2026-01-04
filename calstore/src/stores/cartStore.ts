import { defineStore } from "pinia";
import { ref, computed } from 'vue'
import api from "@/_services/api";

// Interface pour un article du panier
export interface CartItem {
  id: string | number;
  productId?: number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
  maxStock?: number;
}

const useCartStore = defineStore('cart', () => {
    // ==================== STATE ====================
    const cart = ref<CartItem[]>([]);
    const isInitialized = ref(false);
    const isLoading = ref(false);

    // ==================== COMPUTED ====================
    
    // Total d'articles dans le panier
    const totalItems = computed(() => {
        return cart.value.reduce((total, item) => total + item.quantity, 0);
    });

    // Prix total du panier
    const totalPrice = computed(() => {
        return cart.value.reduce((total, item) => total + (item.price * item.quantity), 0);
    });

    // Vérifie si le panier est vide
    const isEmpty = computed(() => cart.value.length === 0);

    // ==================== HELPERS PRIVÉS ====================
    
    /**
     * Normalise un prix en nombre
     */
    const normalizePrice = (p: any): number => {
        if (p === null || p === undefined) return 0;
        if (typeof p === 'number') return p;
        if (typeof p === 'string') {
            const numeric = p.replace(/[^0-9.-]+/g, '');
            const parsed = parseFloat(numeric);
            return isNaN(parsed) ? 0 : parsed;
        }
        return 0;
    };

    /**
     * Normalise un item venant de l'API vers le format CartItem
     */
    const normalizeApiItem = (apiItem: any): CartItem => {
        const product = apiItem.product || {};
        const price = normalizePrice(apiItem.unit_price || apiItem.price || product.price);
        const quantity = typeof apiItem.quantity === 'number' ? apiItem.quantity : 1;
        
        // Récupérer l'image (plusieurs formats possibles)
        let image = null;
        if (product.main_image_url) {
            image = product.main_image_url;
        } else if (apiItem.image) {
            image = apiItem.image;
        } else if (product.images && product.images.length > 0) {
            image = product.images[0].image || product.images[0].url;
        }

        return {
            id: apiItem.id,
            productId: product.id || apiItem.product_id,
            name: product.name || apiItem.name || 'Produit',
            price,
            quantity,
            image,
            maxStock: product.quantity || apiItem.maxStock || null
        };
    };

    /**
     * Sauvegarde le panier dans localStorage
     */
    const saveToLocalStorage = () => {
        if (typeof window !== 'undefined') {
            try {
                localStorage.setItem('cart', JSON.stringify(cart.value));
                console.log('💾 Panier sauvegardé dans localStorage');
            } catch (error) {
                console.error('❌ Erreur lors de la sauvegarde localStorage:', error);
            }
        }
    };

    /**
     * Charge le panier depuis localStorage
     */
    const loadFromLocalStorage = () => {
        if (typeof window !== 'undefined') {
            const savedCart = localStorage.getItem('cart');
            if (savedCart) {
                try {
                    const parsed = JSON.parse(savedCart);
                    cart.value = (parsed || []).map((it: any) => ({
                        id: it.id,
                        productId: it.productId || it.product_id,
                        name: it.name || 'Produit',
                        price: normalizePrice(it.price),
                        quantity: typeof it.quantity === 'number' ? it.quantity : 1,
                        image: it.image || null,
                        maxStock: it.maxStock || null
                    }));
                    console.log('📦 Panier chargé depuis localStorage:', cart.value);
                } catch (error) {
                    console.error('❌ Erreur lors du chargement localStorage:', error);
                    cart.value = [];
                }
            }
        }
    };

    // ==================== ACTIONS API ====================

    /**
     * Récupère le panier depuis le backend
     */
    const fetchCart = async () => {
        isLoading.value = true;
        try {
            console.log('🔄 Récupération du panier depuis le backend...');
            const response = await api.get('/ecommerce/cart/');
            
            console.log('✅ Réponse brute du serveur:', response.data);
            
            const data = response.data.data;
            
            // Normaliser tous les items
            cart.value = (data.items || []).map(normalizeApiItem);
            
            console.log('✅ Panier normalisé:', cart.value);
            
            saveToLocalStorage();
            isInitialized.value = true;
            
            return cart.value;
        } catch (err: any) {
            console.error('❌ Erreur lors de la récupération du panier:', err);
            
            // Si le panier n'existe pas encore (404), c'est normal
            if (err.response?.status === 404 || err.response?.status === 400) {
                console.log('ℹ️ Aucun panier existant, il sera créé au premier ajout');
                cart.value = [];
                isInitialized.value = true;
                return cart.value;
            }
            
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * Ajoute un produit au panier
     */
    const addToCart = async (item: any) => {
        try {
            // Extraire l'ID du produit
            const productId = item.productId || item.product_id || item.id;
            
            if (!productId) {
                console.error('❌ ID produit manquant:', item);
                throw new Error('ID du produit requis');
            }

            const payload: any = {
                product_id: productId,
                quantity: item.quantity || 1
            };

            if (item.variantId || item.variant_id) {
                payload.variant_id = item.variantId || item.variant_id;
            }

            console.log('➕ Ajout au panier:', payload);

            // Note: backend exposes the route at 'cart/add-item/'
            const response = await api.post('/ecommerce/cart/add-item/', payload);
            
            console.log('✅ Réponse ajout:', response.data);

            // Récupérer le panier complet après ajout
            await fetchCart();
            
            return response.data;
        } catch (err: any) {
            console.error('❌ Erreur lors de l\'ajout au panier:', err.response?.data || err.message);
            
            // Fallback : ajout local si l'API échoue
            console.warn('⚠️ Fallback : ajout local');
            
            const localItem: CartItem = {
                id: item.id || `temp-${Date.now()}`,
                productId: item.productId || item.id,
                name: item.name || 'Produit',
                price: normalizePrice(item.price),
                quantity: item.quantity || 1,
                image: item.image || item.main_image_url || null,
                maxStock: item.maxStock || item.quantity || null
            };

            const existingIndex = cart.value.findIndex(cartItem => 
                cartItem.productId === localItem.productId
            );
            
            if (existingIndex !== -1) {
                // Augmenter la quantité si le produit existe déjà
                const existing = cart.value[existingIndex];
                if (existing.maxStock && existing.quantity >= existing.maxStock) {
                    console.warn('⚠️ Stock maximum atteint');
                    throw new Error('Stock maximum atteint');
                }
                existing.quantity += localItem.quantity;
            } else {
                // Ajouter un nouveau produit
                cart.value.push(localItem);
            }
            
            saveToLocalStorage();
            throw err; // Re-throw pour que le composant puisse gérer l'erreur
        }
    };

    /**
     * Met à jour la quantité d'un article
     */
    const updateQuantity = async (itemId: string | number, newQuantity: number) => {
        if (newQuantity <= 0) {
            return removeFromCart(itemId);
        }

        try {
            console.log(`🔄 Mise à jour quantité: item ${itemId} -> ${newQuantity}`);
            
            const response = await api.patch(`/ecommerce/cart/item/${itemId}/`, { 
                quantity: newQuantity 
            });
            
            console.log('✅ Réponse mise à jour:', response.data);
            
            // Mettre à jour localement
            const item = cart.value.find(i => i.id === itemId);
            if (item) {
                item.quantity = newQuantity;
                saveToLocalStorage();
            }
            
            return response.data;
        } catch (err: any) {
            console.error('❌ Erreur mise à jour quantité:', err.response?.data || err.message);
            
            // Fallback local
            const item = cart.value.find(i => i.id === itemId);
            if (item) {
                if (item.maxStock && newQuantity > item.maxStock) {
                    item.quantity = item.maxStock;
                    console.warn('⚠️ Quantité limitée au stock maximum');
                } else {
                    item.quantity = newQuantity;
                }
                saveToLocalStorage();
            }
            
            throw err;
        }
    };

    /**
     * Augmente la quantité d'un article de 1
     */
    const increaseQuantity = async (itemId: string | number) => {
        const item = cart.value.find(i => i.id === itemId);
        if (!item) return;
        
        const newQuantity = item.quantity + 1;
        
        // Vérifier le stock max
        if (item.maxStock && newQuantity > item.maxStock) {
            console.warn('⚠️ Stock maximum atteint');
            return;
        }
        
        return updateQuantity(itemId, newQuantity);
    };

    /**
     * Diminue la quantité d'un article de 1
     */
    const decreaseQuantity = async (itemId: string | number) => {
        const item = cart.value.find(i => i.id === itemId);
        if (!item) return;
        
        const newQuantity = item.quantity - 1;
        
        if (newQuantity <= 0) {
            return removeFromCart(itemId);
        }
        
        return updateQuantity(itemId, newQuantity);
    };

    /**
     * Supprime un article du panier
     */
    const removeFromCart = async (itemId: string | number) => {
        try {
            console.log(`🗑️ Suppression de l'item ${itemId}`);
            
            await api.delete(`/ecommerce/cart/item/${itemId}/`);
            
            console.log('✅ Item supprimé du backend');
            
            // Supprimer localement
            const index = cart.value.findIndex(item => item.id === itemId);
            if (index !== -1) {
                cart.value.splice(index, 1);
                saveToLocalStorage();
            }
        } catch (err: any) {
            console.error('❌ Erreur suppression:', err.response?.data || err.message);
            
            // Fallback local
            const index = cart.value.findIndex(item => item.id === itemId);
            if (index !== -1) {
                cart.value.splice(index, 1);
                saveToLocalStorage();
            }
            
            throw err;
        }
    };

    /**
     * Vide complètement le panier
     */
    const clearCart = async () => {
        try {
            console.log('🗑️ Vidage du panier');
            
            await api.delete('/ecommerce/cart/');
            
            console.log('✅ Panier vidé sur le backend');
        } catch (err: any) {
            console.error('❌ Erreur vidage panier:', err.response?.data || err.message);
        } finally {
            // Toujours vider localement
            cart.value = [];
            localStorage.removeItem('cart');
        }
    };

    // ==================== UTILITAIRES ====================

    /**
     * Vérifie si un produit est dans le panier
     */
    const isInCart = (itemId: string | number) => {
        return cart.value.some(item => item.id === itemId || item.productId === itemId);
    };

    /**
     * Obtient la quantité d'un produit dans le panier
     */
    const getItemQuantity = (itemId: string | number) => {
        const item = cart.value.find(item => 
            item.id === itemId || item.productId === itemId
        );
        return item ? item.quantity : 0;
    };

    /**
     * Initialise le panier (fetch depuis API ou localStorage)
     */
    const initCart = async () => {
        if (isInitialized.value) {
            console.log('ℹ️ Panier déjà initialisé');
            return;
        }

        console.log('🚀 Initialisation du panier...');
        
        try {
            await fetchCart();
            console.log('✅ Panier initialisé depuis le backend');
        } catch (err) {
            console.warn('⚠️ Impossible de récupérer le panier du backend, chargement local');
            loadFromLocalStorage();
            isInitialized.value = true;
        }
    };

    // ==================== AUTO-INITIALISATION ====================
    
    // Initialiser automatiquement au chargement du store
    initCart();

    // ==================== EXPORT ====================
    
    return {
        // State
        cart,
        isInitialized,
        isLoading,
        
        // Computed
        totalItems,
        totalPrice,
        isEmpty,
        
        // Actions API
        fetchCart,
        addToCart,
        updateQuantity,
        increaseQuantity,
        decreaseQuantity,
        removeFromCart,
        clearCart,
        
        // Utilitaires
        isInCart,
        getItemQuantity,
        loadFromLocalStorage,
        initCart
    };
});

export { useCartStore };