from django.urls import path

from .views import CategoryCreateAPIView, ProductListCreateAPIView

urlpatterns = [
    path("categories/", CategoryCreateAPIView.as_view(),
         name="api-category-create"),
    path("products/", ProductListCreateAPIView.as_view(),
         name="api-product-list-create"),
]
