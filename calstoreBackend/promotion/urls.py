from django.urls import path
from .views import (MainPromotionView, ActivePromotionsView, ActiveFlashSalesView, CurrentFlashSaleView)

urlpatterns = [
    # Endpoint pour la promotion "Star" (Bannière)
    path('main/', MainPromotionView.as_view(), name='main-promotion'),
    
    # Endpoint pour la liste des promotions
    path('active/', ActivePromotionsView.as_view(), name='active-promotions'),
    
    # Endpoint pour les ventes flash (Optionnel)
    path('flash-sales/', ActiveFlashSalesView.as_view(), name='flash-sales'),

    path('flash-sales/current/', CurrentFlashSaleView.as_view(), name='current-flash-sale'), # ← nouveau
]