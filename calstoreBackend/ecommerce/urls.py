from django.urls import path
from .views import *

urlpatterns = [
    path('', view=index, name="index"),
    path('category-details', view=CategoryListAPIView.as_view(), name="category-detail")
]
