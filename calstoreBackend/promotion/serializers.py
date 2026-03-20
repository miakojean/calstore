# promotions/serializers.py
from rest_framework import serializers
from .models import Promotion, FlashSale, FlashSaleProduct
from ecommerce.serializers import ProductSerializer
from ecommerce.models import Product

class PromotionSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Promotion
        fields = [
            'id', 'name', 'description', 'promotion_type', 
            'discount_percentage', 'discount_amount', 'products',
            'start_date', 'end_date', 'code', 'status', 'is_active',
            'is_valid', 'products_count', 'created_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'usage_count']


class FlashSaleProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product',
        write_only=True
    )
    
    class Meta:
        model = FlashSaleProduct
        fields = ['id', 'product', 'product_id', 'flash_price', 'stock_limit', 'sold_quantity']


class FlashSaleSerializer(serializers.ModelSerializer):
    products = FlashSaleProductSerializer(many=True, read_only=True, source='flashsaleproduct_set')
    is_ongoing = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = FlashSale
        fields = [
            'id', 
            'name', 
            'products', 
            'start_time', 
            'end_time', 
            'is_active', 
            'is_ongoing',
            'image',
        ]
        read_only_fields = ['id','created_at', 'updated_at']

# promotions/serializers.py

class FlashSaleSimpleSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = FlashSale
        fields = ['id', 'name', 'image', 'start_time', 'end_time', 'products']

    def get_products(self, obj):
        # On récupère le request pour générer des URLs absolues (http://...)
        request = self.context.get('request')
        items = obj.flashsaleproduct_set.select_related('product').all()
        
        product_list = []
        for item in items:
            # On récupère l'objet image (votre ProductImage)
            image_obj = item.product.main_image
            image_url = None
            
            if image_obj:
                # Si image_obj est l'instance, et qu'elle a un champ 'image' (ImageField)
                # On essaie de récupérer l'URL. Adaptez 'image' au nom de votre champ.
                try:
                    if hasattr(image_obj, 'image') and image_obj.image:
                        image_url = image_obj.image.url
                    else:
                        # Si main_image renvoie directement un ImageField
                        image_url = image_obj.url
                        
                    # Transformer en URL complète (avec le domaine) si possible
                    if image_url and request:
                        image_url = request.build_absolute_uri(image_url)
                except (AttributeError, ValueError):
                    image_url = None

            product_list.append({
                "id": item.product.id,
                "name": item.product.name,
                "slug": item.product.slug,
                "original_price": item.product.price,
                "flash_price": item.flash_price,
                "stock_limit": item.stock_limit,
                "sold_quantity": item.sold_quantity,
                "image": image_url, # Maintenant c'est une chaîne de caractères (URL)
                "in_stock": item.product.in_stock,
            })
        return product_list