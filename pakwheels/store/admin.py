from django.contrib import admin

from .models import (
    CarModel,
    Category,
    Favorite,
    Feature,
    Like,
    Product,
    ProductFeature,
    ProductImage,
    Rating,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "modified")
    search_fields = ("name", "slug")
    list_filter = ("parent",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "make", "name", "variant", "modified")
    search_fields = ("make", "name", "variant", "slug")
    list_filter = ("make",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "seller", "category", "status", "price", "is_active", "modified")
    list_filter = ("status", "is_active", "condition", "category")
    search_fields = ("title", "slug", "seller__email", "ad_reference_id")
    autocomplete_fields = ("seller", "category", "model")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "modified")
    search_fields = ("product__title", "product__slug")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "modified")
    search_fields = ("user__email", "product__title")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "modified")
    search_fields = ("user__email", "product__title")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "score", "modified")
    list_filter = ("score",)
    search_fields = ("user__email", "product__title")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "modified")
    search_fields = ("name", "slug")


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "feature", "modified")
    search_fields = ("product__title", "feature__name")
