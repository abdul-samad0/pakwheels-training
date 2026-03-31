from django.utils.text import slugify
from rest_framework import serializers

from pakwheels.store.models import Category, Product, Like, Favorite, Rating
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


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    model_name = serializers.CharField(source="model.name", read_only=True)
    make_name = serializers.CharField(source="model.make", read_only=True)
    seller_email = serializers.EmailField(
        source="seller.email", read_only=True)
    images = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def get_like_count(self, obj):
        return Like.objects.filter(product=obj).count()

    def get_favorite_count(self, obj):
        return Favorite.objects.filter(product=obj).count()

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
            "created",
            "category",
            "model_name",
            "make_name",
            "seller_email",
            "images",
            "like_count",
            "favorite_count",
        )


class LikeSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="slug", queryset=Product.objects.filter(is_active=True))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    validators = []  # disable unique_together pre-validation for toggle

    class Meta:
        model = Like
        fields = ("id", "product", "user")
        read_only_fields = ("id",)

    def create(self, validated_data):
        product = validated_data["product"]
        user = validated_data["user"]
        like = Like.objects.filter(product=product, user=user).first()

        if like:
            like.delete()
            is_liked = False
        else:
            Like.objects.create(product=product, user=user)
            is_liked = True

        like_count = Like.objects.filter(product=product).count()
        return {
            "product_id": product.id,
            "is_liked": is_liked,
            "like_count": like_count,
            "message": "Liked" if is_liked else "Unliked",
        }


class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="slug", queryset=Product.objects.filter(is_active=True))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    validators = []  # disable unique_together pre-validation for toggle

    class Meta:
        model = Favorite
        fields = ("id", "product", "user")
        read_only_fields = ("id",)

    def create(self, validated_data):
        product = validated_data["product"]
        user = validated_data["user"]
        favorite = Favorite.objects.filter(product=product, user=user).first()

        if favorite:
            favorite.delete()
            is_favorited = False
        else:
            Favorite.objects.create(product=product, user=user)
            is_favorited = True

        favorite_count = Favorite.objects.filter(product=product).count()
        return {
            "product_id": product.id,
            "is_favorited": is_favorited,
            "favorite_count": favorite_count,
            "message": "Added to favorites" if is_favorited else "Removed from favorites",
        }


class RatingSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="slug", queryset=Product.objects.filter(is_active=True))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    validators = []

    class Meta:
        model = Rating
        fields = ("id", "product", "user", "score")
        read_only_fields = ("id",)

    def create(self, validated_data):
        product = validated_data["product"]
        user = validated_data["user"]
        score = validated_data["score"]
        rating = Rating.objects.filter(product=product, user=user).first()

        if rating:
            rating.score = score
            rating.save()
        else:
            Rating.objects.create(product=product, user=user, score=score)
        return rating
