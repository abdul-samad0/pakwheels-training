from django.db import models


class ProductCondition(models.TextChoices):
    NEW = "new", "New"
    USED = "used", "Used"


class TransmissionType(models.TextChoices):
    MANUAL = "manual", "Manual"
    AUTOMATIC = "automatic", "Automatic"


class FuelType(models.TextChoices):
    PETROL = "petrol", "Petrol"
    DIESEL = "diesel", "Diesel"
    HYBRID = "hybrid", "Hybrid"
    ELECTRIC = "electric", "Electric"
    CNG = "cng", "CNG"
    LPG = "lpg", "LPG"


class AssemblyType(models.TextChoices):
    LOCAL = "local", "Local"
    IMPORTED = "imported", "Imported"


class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    SOLD = "sold", "Sold"
    ARCHIVED = "archived", "Archived"
