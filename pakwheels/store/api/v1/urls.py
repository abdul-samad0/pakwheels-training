from django.urls import path

from .views import CategoryCreateAPIView, ProductCreateAPIView, ProductListAPIView

urlpatterns = [
    path("categories/", CategoryCreateAPIView.as_view(), name="api-category-create"),
    path("products/", ProductListAPIView.as_view(), name="api-product-list"),
    path("products/add/", ProductCreateAPIView.as_view(), name="api-product-create"),
]
