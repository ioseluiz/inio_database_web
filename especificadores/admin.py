from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import EspecificadorResource

from .models import Especificador

@admin.register(Especificador)
class EstimadorAdmin(ImportExportModelAdmin):
    resource_class = EspecificadorResource
    list_display = ('nombre', 'iniciales','is_active')
    search_fields = ('nombre', 'iniciales')
