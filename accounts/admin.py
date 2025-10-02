from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Додаткова інформація", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Додаткова інформація", {"fields": ("role",)}),
    )

    search_fields = ("username", "email")
    ordering = ("username",)

    def save_model(self, request, obj, form, change):
        # Auto-update staff status depending on role
        if obj.role == "admin":
            obj.is_staff = True
        else:
            obj.is_staff = False
        super().save_model(request, obj, form, change)
