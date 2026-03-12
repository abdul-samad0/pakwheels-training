from django.db import models
from django_extensions.db.models import TimeStampedModel

from .choices import (
    AssemblyType,
    FuelType,
    ProductCondition,
    ProductStatus,
    TransmissionType,
)


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    parent = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories"
    )

    def __str__(self):
        return self.name


class CarModel(TimeStampedModel):
    make = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    variant = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ("make", "name", "variant")

    def __str__(self):
        return f"{self.make} {self.name} {self.variant}".strip()


class Product(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    ad_reference_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    assembly_type = models.CharField(
        max_length=20, choices=AssemblyType.choices, null=True, blank=True
    )
    auction_grade = models.CharField(max_length=20, blank=True)
    body_type = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    condition = models.CharField(max_length=10, choices=ProductCondition.choices)
    fuel_type = models.CharField(
        max_length=20, choices=FuelType.choices, null=True, blank=True
    )
    location = models.CharField(max_length=100)
    registered_city = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=ProductStatus.choices, default=ProductStatus.ACTIVE
    )
    title = models.CharField(max_length=255)
    transmission = models.CharField(
        max_length=20, choices=TransmissionType.choices, null=True, blank=True
    )
    listed_at = models.DateTimeField(null=True, blank=True)
    fuel_average = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    engine_capacity_cc = models.PositiveIntegerField(null=True, blank=True)
    mileage = models.PositiveIntegerField(help_text="Mileage in kilometers", null=True, blank=True)
    import_year = models.PositiveSmallIntegerField(null=True, blank=True)
    registered_year = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="products"
    )
    model = models.ForeignKey(
        "CarModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    seller = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="products"
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["created"]),
            models.Index(fields=["status"]),
            models.Index(fields=["year"]),
        ]

    def __str__(self):
        return self.title


class Feature(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Favorite(TimeStampedModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")


class Like(TimeStampedModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")


class ProductFeature(TimeStampedModel):
    feature = models.ForeignKey(
        "Feature",
        on_delete=models.CASCADE,
        related_name="product_features"
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="product_features"
    )

    class Meta:
        unique_together = ("product", "feature")


class ProductImage(TimeStampedModel):
    image = models.ImageField(upload_to="products/")
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="images"
    )

    def __str__(self):
        return f"Image for {self.product.title}"


class Rating(TimeStampedModel):
    score = models.IntegerField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")
