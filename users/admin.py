from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'is_manager')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_manager')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('is_manager',)}),
    )
