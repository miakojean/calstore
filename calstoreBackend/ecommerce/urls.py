from django.urls import path
from .views import (CategoryDetailAPIView, CategoryListAPIView)

urlpatterns = [
    path('category-list', view=CategoryListAPIView.as_view(), name="category-list"),
    path('category-details', view=CategoryDetailAPIView.as_view(), name="category-details")
]
