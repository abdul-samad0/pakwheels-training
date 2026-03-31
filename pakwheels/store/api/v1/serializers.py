from django.utils.text import slugify
from rest_framework import serializers

from pakwheels.store.models import Category, Product
from pakwheels.store.utils import make_unique_slug


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent")
        read_only_fields = ("id",)

    def validate_slug(self, value):
        if value and Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                "Category with this slug already exists.")
        return value

    def create(self, validated_data):
        provided_slug = validated_data.pop("slug", "")
        if provided_slug:
            return Category.objects.create(**validated_data, slug=provided_slug)

        else:
            name = validated_data.get("name", "")
            base_slug = slugify(name) or "category"
            slug = make_unique_slug(base_slug, Category)
            validated_data["slug"] = slug
            return Category.objects.create(**validated_data)


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
    model_name = serializers.CharField(source="model.name", read_only=True)
    seller_email = serializers.EmailField(
        source="seller.email", read_only=True)

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

