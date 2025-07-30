from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_CC_Resource, Proyecto_CC_Estimado_Conceptal_Resource

from .models import Proyecto_CC, Proyecto_CC_Estimado_Conceptual

@admin.register(Proyecto_CC)
class Proyecto_CCAdmin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Resource
    list_display = ('codigo','title','fecha_entrada','fecha_envio_FIO','seccion','coordinador','estado','asignacion_presup_final','precio_acp')
    search_fields =('codigo','title')

@admin.register(Proyecto_CC_Estimado_Conceptual)
class Proyecto_CC_Estimado_Conceptual_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Estimado_Conceptal_Resource
    list_display = ('proyecto_cc', 'estimado_conceptual')
    search_fields = ('proyecto_cc__codigo', 'estimado_conceptual__codigo')
    autocomplete_fields = ['proyecto_cc', 'estimado_conceptual']
