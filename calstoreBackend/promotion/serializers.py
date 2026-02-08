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
        fields = ['id', 'name', 'products', 'start_time', 'end_time', 'is_active', 'is_ongoing']