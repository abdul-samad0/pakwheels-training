from django.db import models
from django_extensions.db.models import TimeStampedModel

from .choices import ProductCondition


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


class Product(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    condition = models.CharField(max_length=10, choices=ProductCondition.choices)
    location = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    category = models.ForeignKey(
        "Category",
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
        ]

    def __str__(self):
        return self.title


class ProductImage(TimeStampedModel):
    image = models.ImageField(upload_to="products/")

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="images"
    )

    def __str__(self):
        return f"Image for {self.product.title}"


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


class Rating(TimeStampedModel):
    score = models.IntegerField()

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")
