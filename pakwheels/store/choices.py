from django.db import models


class ProductCondition(models.TextChoices):
    NEW = "new", "New"
    USED = "used", "Used"

