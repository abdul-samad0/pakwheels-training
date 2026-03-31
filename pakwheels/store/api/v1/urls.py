from django.urls import path

from .views import CategoryCreateAPIView, ProductListCreateAPIView, ProductDetailAPIView, ProductLikeAPIView, ProductFavoriteAPIView, RatingCreateAPIView

urlpatterns = [
    path("categories/", CategoryCreateAPIView.as_view(),
         name="api-category-create"),
    path("products/", ProductListCreateAPIView.as_view(),
         name="api-product-list-create"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(),
         name="api-product-detail"),
    path("products/<slug:slug>/like/", ProductLikeAPIView.as_view(),
         name="api-product-like"),
    path("products/<slug:slug>/favorite/", ProductFavoriteAPIView.as_view(),
         name="api-product-favorite"),
    path("products/<slug:slug>/rating/", RatingCreateAPIView.as_view(),
         name="api-product-rating"),
]
