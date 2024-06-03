from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser


class AppUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ("App Settings", {
            "fields": ("is_business",)},
         ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "is_business"),
            },
        ),
    )
    list_display = ("username", "email", "is_business", "is_staff")
    list_filter = (*UserAdmin.list_filter, "is_business")


admin.site.register(AppUser, AppUserAdmin)
