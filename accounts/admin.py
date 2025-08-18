# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Formularios a usar
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Campos a mostrar en la lista de usuarios
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username',)
    ordering = ('email',)

    # CAMPOS PARA LA PÁGINA DE EDICIÓN
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # CAMPOS PARA LA PÁGINA DE CREACIÓN
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)