from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_CC_Resource, Proyecto_CC_Estimado_Conceptal_Resource, Proyecto_CC_Licitacion_Resource, Proyecto_CC_Licitacion_V2_Resource, Proyecto_CC_SIA_Resource, Proyecto_CC_Secciones_MF_Resource, Proyecto_CC_Cronograma_Resource, Proyecto_CC_Fechas_Actual_Resource

from .models import Proyecto_CC, Proyecto_CC_Estimado_Conceptual, Proyecto_CC_Licitacion, Proyecto_CC_Licitacion_V2, Proyecto_CC_SIA, Proyecto_CC_Secciones_MF, Proyecto_CC_Cronograma, Proyecto_CC_Fechas_Actual

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

@admin.register(Proyecto_CC_Licitacion_V2)
class Proyecto_CC_Licitacion_V2_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Licitacion_V2_Resource
    list_display = ('proyecto_cc', 'licitacion')
    search_fields = ('proyecto_cc__codigo', 'licitacion__rfq')
    autocomplete_fields = ['proyecto_cc', 'licitacion']

@admin.register(Proyecto_CC_SIA)
class Proyecto_CC_SIA_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_SIA_Resource
    list_display = ('proyecto_cc', 'sia')
    search_fields = ('proyecto_cc__codigo', 'sia__CodProyecto')
    autocomplete_fields = ['proyecto_cc', 'sia']

@admin.register(Proyecto_CC_Secciones_MF)
class Proyecto_CC_Secciones_MF_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Secciones_MF_Resource
    list_display = ('proyecto_cc','seccion')
    search_fields = ('proyecto_cc__codigo','seccion')
    autocomplete_fields = ['proyecto_cc']

@admin.register(Proyecto_CC_Cronograma)
class Proyecto_CC_Cronograma_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Cronograma_Resource
    list_display = ('proyecto_cc', 'inicio', 'entrega_50_porciento',
                    'entrega_90_porciento', 'entrega_owner')
    search_fields = ('proyecto_cc__codigo',)
    autocomplete_fields = ['proyecto_cc']

@admin.register(Proyecto_CC_Fechas_Actual)
class Proyecto_CC_Fechas_Actual_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Fechas_Actual_Resource
    list_display = ('proyecto_cc', 'inicio_actual', 'entrega_50_porciento_actual',
                    'entrega_90_porciento_actual', 'inicio_division_review',
                    'fin_division_review')
    search_fields = ('proyecto_cc__codigo',)
    autocomplete_fields = ['proyecto_cc']