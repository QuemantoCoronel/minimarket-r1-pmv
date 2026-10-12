from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    list_display = ("email", "display_name", "role", "is_active")
    list_filter = ("role", "is_active")
    ordering = ("email_normalized",)
    search_fields = ("email", "display_name")
    fieldsets = (
        (None, {"fields": ("email", "password")} ),
        ("Perfil", {"fields": ("display_name", "role")} ),
        ("Estado", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")} ),
        ("Fechas", {"fields": ("last_login", "created_at", "updated_at")} ),
    )
    readonly_fields = ("created_at", "updated_at")
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "display_name", "role", "password1", "password2")} ),)

