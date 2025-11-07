from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_CC_Resource, Proyecto_CC_Estimado_Conceptal_Resource, Proyecto_CC_Licitacion_Resource, Proyecto_CC_SIA_Resource

from .models import Proyecto_CC, Proyecto_CC_Estimado_Conceptual, Proyecto_CC_Licitacion, Proyecto_CC_SIA

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

@admin.register(Proyecto_CC_Licitacion)
class Proyecto_CC_Licitacion_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Licitacion_Resource
    list_display = ('proyecto_cc', 'licitacion')
    search_fields = ('proyecto_cc__codigo', 'licitacion__rfq')
    autocomplete_fields = ['proyecto_cc', 'licitacion']

@admin.register(Proyecto_CC_SIA)
class Proyecto_CC_SIA_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_SIA_Resource
    list_display = ('proyecto_cc', 'sia')
    search_fields = ('proyecto_cc__codigo', 'sia__CodProyecto')
    autocomplete_fields = ['proyecto_cc', 'sia']

