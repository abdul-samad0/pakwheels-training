from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    """Registration form for custom User (email-based, no username)."""

    class Meta:
        model = User
        fields = ["email", "phone", "password1", "password2"]
