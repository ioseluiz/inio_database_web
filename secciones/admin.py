from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import SeccionResource

from .models import Seccion

@admin.register(Seccion)
class SeccionAdmin(ImportExportModelAdmin):
    resource_class = SeccionResource
    list_display = ('name', 'is_active')
    search_fields = ('name', 'is_active')