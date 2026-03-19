from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    AccountPasswordChangeForm,
    ProfileForm,
    ProfileImageForm,
    ProfileUserForm,
    UserRegistrationForm,
)
from .models import Profile, ProfileImage


def register_view(request):
    """Render registration form; on valid POST create user and redirect to login."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard_view(request):
    """
    Placeholder protected page for testing auth.
    Uses @login_required and request.user; replace with real functionality later.
    """
    return render(request, "accounts/dashboard.html", {"user": request.user})


@login_required
def profile_view(request):
    """Update user profile details, image, and password in one page."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile_image = ProfileImage.objects.filter(profile=profile).first()
    user_form = ProfileUserForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)
    image_form = ProfileImageForm()
    password_form = AccountPasswordChangeForm(request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            user_form = ProfileUserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=profile)
            image_form = ProfileImageForm(request.POST, request.FILES)
            if user_form.is_valid() and profile_form.is_valid() and image_form.is_valid():
                user_form.save()
                profile_form.save()
                image = image_form.cleaned_data.get("image")
                if image:
                    if profile_image:
                        profile_image.image = image
                        profile_image.save()
                    else:
                        ProfileImage.objects.create(profile=profile, image=image)
                return redirect("profile")
        elif "change_password" in request.POST:
            password_form = AccountPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "image_form": image_form,
            "profile": profile,
            "profile_form": profile_form,
            "profile_image": profile_image,
            "user_form": user_form,
            "password_form": password_form,
        },
    )
