from django.urls import path
from .views import (
    CategoryDetailAPIView, 
    CategoryListAPIView, 
    CategoryProductsAPIView, 
    CheckoutAPIView,
    CartAPIView,
    AddToCartAPIView,
    CartItemAPIView
)

urlpatterns = [
    path('category-list', view=CategoryListAPIView.as_view(), name="category-list"),
    
    # Changement ici : ajouter <slug:slug> pour accepter le paramètre
    path('category-details/<slug:slug>', view=CategoryDetailAPIView.as_view(), name="category-details"),
    
    # Ajoutez aussi cette URL si vous voulez utiliser CategoryProductsAPIView
    path('category-products/<slug:slug>', view=CategoryProductsAPIView.as_view(), name="category-products"),

    # About Cart
    path('cart/', view=CartAPIView.as_view(), name="cart"),
    path('cart/add-item/', view=AddToCartAPIView.as_view(), name="add-to-cart"),
    path('cart/item/<int:item_id>/', view=CartItemAPIView.as_view(), name="cart-item"),
    
    # URL pour le checkout
    path('checkout/', view=CheckoutAPIView.as_view(), name="checkout"),
]