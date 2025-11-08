from django.contrib import admin
from .models import (
    Category, 
    Brand,
    Product,
    ProductImage,
    ProductVariant,
    GuestCustomer,
    Customer,
    Address,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review
)
# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)