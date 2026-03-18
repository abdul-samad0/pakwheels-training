from django.urls import path

from .views import (
    category_add_view,
    favorite_list_view,
    favorite_toggle_view,
    product_add_view,
    product_detail_view,
    product_list_view,
)

urlpatterns = [
    path("products/", product_list_view, name="product_list"),
    path("products/add/", product_add_view, name="product_add"),
    path("products/<slug:slug>/", product_detail_view, name="product_detail"),
    path("categories/add/", category_add_view, name="category_add"),
    path("products/<slug:slug>/favorite/", favorite_toggle_view, name="favorite_toggle"),
    path("favorites/", favorite_list_view, name="favorite_list"),
]
