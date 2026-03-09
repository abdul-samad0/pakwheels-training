from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(TimeStampedModel):
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} Profile"


class ProfileImage(TimeStampedModel):
    image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} Profile Image"
