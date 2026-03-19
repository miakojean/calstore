from django.contrib import admin
from .models import (Promotion, UserPromotionUsage, FlashSale, FlashSaleProduct)

# Register your models here.

admin.site.register(Promotion)
admin.site.register(UserPromotionUsage)
admin.site.register(FlashSale)
admin.site.register(FlashSaleProduct)