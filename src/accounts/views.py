from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


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
