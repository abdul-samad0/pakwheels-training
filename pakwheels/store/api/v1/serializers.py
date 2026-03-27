from django.utils.text import slugify
from rest_framework import serializers

from pakwheels.store.models import Category, Product
from pakwheels.store.utils import make_unique_slug


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent")
        read_only_fields = ("id", "slug")

    def create(self, validated_data):
        category = Category(**validated_data)
        base_slug = slugify(category.name) or "category"
        category.slug = make_unique_slug(base_slug, Category)
        category.save()
        return category


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "price",
            "location",
            "condition",
            "category",
            "model",
            "status",
            "fuel_type",
            "transmission",
            "assembly_type",
            "year",
            "mileage",
            "engine_capacity_cc",
            "registered_city",
            "body_type",
            "color",
            "listed_at",
            "is_active",
            "is_featured",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        request = self.context["request"]
        product = Product(**validated_data)
        product.seller = request.user
        base_slug = slugify(product.title) or "product"
        product.slug = make_unique_slug(base_slug, Product)
        product.save()
        return product


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    model_name = serializers.SerializerMethodField()
    seller_email = serializers.EmailField(source="seller.email", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "price",
            "condition",
            "status",
            "location",
            "registered_city",
            "year",
            "mileage",
            "fuel_type",
            "transmission",
            "assembly_type",
            "body_type",
            "color",
            "is_featured",
            "created",
            "category",
            "model_name",
            "seller_email",
        )

    def get_model_name(self, obj):
        if not obj.model_id:
            return None
        return str(obj.model)
