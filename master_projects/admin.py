
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Master_Proyecto_Resource

from .models import MasterProject

@admin.register(MasterProject)
class Master_Proyecto_Admin(ImportExportModelAdmin):
    resource_class = Master_Proyecto_Resource
    list_display = ('unidad_solicitante','nip','proyecto_cc','fecha_estimada_entrega_owner','fiscal_year','comentarios','estado')
    search_fields =('proyecto_cc','nip')
    autocomplete_fields = ['proyecto_cc']