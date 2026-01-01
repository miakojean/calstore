# serializers.py
from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant

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