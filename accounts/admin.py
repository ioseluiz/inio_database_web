from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("email","username","is_staff")
    search_fields = ("email","username")
    list_filter = ("is_staff","is_active")

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
              "fields": ("email","username","password1","password2"),
              },
              )
    )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determina la respuesta HTTP después de que un objeto ha sido añadido con éxito.
        Sobrescribe para redirigir a la lista de usuarios en lugar de a la página de edición.
        """
        # Construye la URL para la vista de lista (changelist) de tu modelo de usuario
        # Reemplaza 'tu_app_label' con el nombre real de tu app (ej: 'accounts', 'users')
        # Reemplaza 'tumodelocustomuser' con el nombre de tu modelo en minúsculas
        opts = self.model._meta
        changelist_url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
        # Redirige a la lista de usuarios
        return HttpResponseRedirect(changelist_url)
    
admin.site.register(CustomUser, CustomUserAdmin)

