from django.urls import path

from .views import product_list_view, product_add_view

urlpatterns = [
    path("products/", product_list_view, name="product_list"),
    path("products/add/", product_add_view, name="product_add"),
]
