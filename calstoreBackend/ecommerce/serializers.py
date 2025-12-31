# serializers.py
from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Category
    """
    
    # Champ calculé pour l'URL complète de l'image
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'image_url',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """
        Retourne l'URL complète de l'image si elle existe
        """
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    """
    Serializer pour Category incluant les produits associés
    """
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'is_active',
            'products'
        ]
    
    def get_products(self, obj):
        """
        Retourne la liste des produits associés à cette catégorie
        """
        products = obj.products.filter(is_active=True)
        return ProductSerializer(products, many=True, context=self.context).data

# --- 1. Sérialiseurs de base (Helpers) ---

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'order']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'value', 'sku', 'price_modifier', 'quantity', 'is_active']

# --- 2. Sérialiseur Principal Produit ---

class ProductSerializer(serializers.ModelSerializer):
    # Relations imbriquées (Nested) : Pour avoir l'objet complet et pas juste l'ID
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    
    # Images et Variantes
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    # Champs calculés (Properties définies dans le modèle)
    is_on_sale = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    
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