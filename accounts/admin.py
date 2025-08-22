from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # what fields to show in list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # fieldsets control how forms look in the admin
    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ('role',)}),
    )

    # fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Додаткова інформація', {'fields': ('role',)}),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
