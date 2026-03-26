from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import dashboard_view, profile_view, register_view

urlpatterns = [
    path("api/v1/", include("pakwheels.accounts.api.v1.urls")),
    path("register/", register_view, name="register"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
]
