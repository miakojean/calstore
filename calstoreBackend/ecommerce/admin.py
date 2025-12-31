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
admin.site.register(ProductVariant)
admin.site.register(GuestCustomer)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)