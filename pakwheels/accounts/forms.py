from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

from .models import Profile, User


class UserRegistrationForm(UserCreationForm):
    """Registration form for custom User (email-based, no username)."""

    class Meta:
        model = User
        fields = ["email", "phone", "password1", "password2"]


class ProfileUserForm(forms.ModelForm):
    """Update basic user account information."""

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone"]


class ProfileForm(forms.ModelForm):
    """Update profile details."""

    class Meta:
        model = Profile
        fields = ["city", "location"]


class ProfileImageForm(forms.Form):
    """Upload or replace profile image."""

    image = forms.ImageField(required=False)


class AccountPasswordChangeForm(PasswordChangeForm):
    """Password change form wrapper for account settings page."""
    pass
