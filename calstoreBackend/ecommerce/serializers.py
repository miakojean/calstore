# serializers.py
from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductImage, ProductVariant,
    Order, OrderItem, Customer, GuestCustomer, Address, Cart, CartItem
)

# --- Sérialiseurs de base ---

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'order']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'value', 'sku', 'price_modifier', 'quantity', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    # Relations imbriquées pour l'affichage (lecture seule)
    category = serializers.StringRelatedField()  # Affiche le nom de la catégorie
    brand = BrandSerializer(read_only=True)
    
    # Images et Variantes
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    # Champs calculés (Properties du modèle)
    is_on_sale = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    main_image = serializers.SerializerMethodField()
    
    # Champs pour les URLs d'images
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'category', 'brand', 'price', 'compare_price', 'quantity',
            'is_active', 'is_featured', 'is_on_sale', 'discount_percentage',
            'in_stock', 'main_image', 'main_image_url', 'images', 'variants', 
            'created_at', 'weight', 'dimensions', 'meta_title', 'meta_description'
        ]
    
    def get_main_image(self, obj):
        main_img = obj.main_image
        if main_img:
            request = self.context.get('request')
            return ProductImageSerializer(main_img, context={'request': request}).data
        return None
    
    def get_main_image_url(self, obj):
        """
        Retourne l'URL de l'image principale directement 
        pour éviter de devoir boucler sur le tableau 'images' en front.
        """
        request = self.context.get('request')
        main_img = obj.main_image  # Utilise la property du modèle
        
        if main_img and main_img.image:
            if request:
                return request.build_absolute_uri(main_img.image.url)
            return main_img.image.url
        return None

# --- Sérialiseurs pour Catégorie ---

class CategorySerializer(serializers.ModelSerializer):
    """
    Sérialiseur simple pour le modèle Category.
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 
            'image', 'image_url', 'is_active', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour une catégorie qui inclut la liste de ses produits.
    """
    products = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 
            'image_url', 'is_active', 'products', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_products(self, obj):
        # Récupérer seulement les produits actifs
        products = obj.products.filter(is_active=True).order_by('-created_at')[:50]  # Limite à 50 produits
        request = self.context.get('request')
        return ProductSerializer(products, many=True, context={'request': request}).data

# --- Sérialiseurs pour Catégorie ---

# --- Serialiseur pour la cart ---
# --- Serializers pour Cart ---

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    # Pour l'ajout/modification d'items
    product_id = serializers.IntegerField(write_only=True)
    variant_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'variant', 'quantity', 
            'unit_price', 'total_price', 'added_at',
            'product_id', 'variant_id'
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'customer', 'guest_customer', 'session_key',
            'items', 'total_items', 'subtotal', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddToCartSerializer(serializers.Serializer):
    """Serializer pour ajouter un produit au panier"""
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produit introuvable ou inactif.")
        return value

    def validate_variant_id(self, value):
        if value:
            try:
                ProductVariant.objects.get(id=value, is_active=True)
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError("Variante introuvable ou inactive.")
        return value

class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer pour modifier la quantité d'un item"""
    quantity = serializers.IntegerField(min_value=1)

class CategorySerializer(serializers.ModelSerializer):
    """
    Sérialiseur simple pour le modèle Category.
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 
            'image', 'image_url', 'is_active'
        ]
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour une catégorie qui inclut la liste de ses produits.
    """
    products = ProductSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 
            'image_url', 'is_active', 'products'
        ]
        
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    
    # Champ spécifique pour faciliter l'affichage de l'image principale en front
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'slug', 
            'description', 
            'short_description',
            'price', 
            'compare_price', 
            'cost_price',
            'discount_percentage',
            'is_on_sale',
            'in_stock',
            'sku',
            'quantity',
            'low_stock_threshold',
            'category', 
            'brand',
            'images',
            'main_image_url', # Champ custom ajouté ci-dessous
            'variants',
            'weight',
            'dimensions',
            'meta_title',
            'meta_description',
            'is_featured',
            'is_digital',
            'published_at'
        ]

    def get_main_image_url(self, obj):
        """
        Retourne l'URL de l'image principale directement 
        pour éviter de devoir boucler sur le tableau 'images' en front.
        """
        request = self.context.get('request')
        main_img = obj.main_image # Utilise la property du modèle
        
        if main_img and main_img.image:
            if request:
                return request.build_absolute_uri(main_img.image.url)
            return main_img.image.url
        return None
    
# --- Serialiseur pour la gestion des commandes (Orders) ---

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = serializers.StringRelatedField()  # Affiche une représentation lisible du client

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'status', 
            'total_price', 'created_at', 'updated_at', 'items'
        ]
    
# --- Serialiseur pour le checkout ---
class CheckoutSerializer(serializers.Serializer):
    """
    Sérialiseur pour gérer les données du checkout ou la validation de la commande.
    """
    cart_id = serializers.UUIDField()
    shipping_address = serializers.CharField(required=False,max_length=500, allow_blank=True)
    billing_address = serializers.CharField(required=False,max_length=500, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=['credit_card', 'paypal', 'stripe', 'A la livraison'],
        required=False,
        default='A la livraison'
    )
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20, required=False)
    special_instructions = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    apply_discount_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    agree_terms = serializers.BooleanField()
    subscribe_newsletter = serializers.BooleanField(required=False)
    gift_option = serializers.BooleanField(required=False)
    gift_message = serializers.CharField(max_length=500, required=False, allow_blank=True)
    save_info = serializers.BooleanField(required=False)
    preferred_delivery_date = serializers.DateField(required=False)
    preferred_delivery_time = serializers.TimeField(required=False)
    referral_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    marketing_consent = serializers.BooleanField(required=False)
    device_info = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_agree_terms(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the terms and conditions.")
        return value
    
    def validate_cart_id(self, value):
        # Ici, vous pouvez ajouter une logique pour vérifier si le panier existe
        from .models import Cart
        try:
            cart = Cart.objects.get(id=value)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Invalid cart ID.")
        return value
    # Vous pouvez ajouter d'autres validations personnalisées si nécessaire 
