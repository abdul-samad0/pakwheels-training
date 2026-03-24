from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Profile, ProfileImage, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "email", "first_name", "last_name",
                    "phone", "is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name", "phone")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("is_active", "is_staff",
         "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "city", "location", "modified")
    list_filter = ("city",)
    raw_id_fields = ("user",)
    search_fields = ("user__email", "city", "location")


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "modified")
    raw_id_fields = ("profile",)
    search_fields = ("profile__user__email",)
