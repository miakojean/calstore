from django.urls import path
from .views import MainPromotionView, ActivePromotionsView, ActiveFlashSalesView

urlpatterns = [
    # Endpoint pour la promotion "Star" (Bannière)
    path('main/', MainPromotionView.as_view(), name='main-promotion'),
    
    # Endpoint pour la liste des promotions
    path('active/', ActivePromotionsView.as_view(), name='active-promotions'),
    
    # Endpoint pour les ventes flash (Optionnel)
    path('flash-sales/', ActiveFlashSalesView.as_view(), name='flash-sales'),
]