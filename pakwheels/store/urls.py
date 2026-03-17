from django.urls import path

from .views import category_add_view, product_add_view, product_list_view

urlpatterns = [
    path("products/", product_list_view, name="product_list"),
    path("products/add/", product_add_view, name="product_add"),
    path("categories/add/", category_add_view, name="category_add"),
]
