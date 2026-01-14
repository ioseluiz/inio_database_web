from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_E_Resource, HorasApoyo_Resource, Proyecto_E_SIA_Resource

from .models import Proyecto_E, HorasApoyo, Proyecto_E_SIA



@admin.register(Proyecto_E)
class Proyecto_EAdmin(ImportExportModelAdmin):
    resource_class = Proyecto_E_Resource
    list_display = ('codigo','title','fecha_entrada','fecha_salida','seccion','coordinador','bldg')
    search_fields =('codigo','title')

@admin.register(HorasApoyo)
class Proyecto_E_HorasApoyo_Resource(ImportExportModelAdmin):
    resource_class = HorasApoyo_Resource
    list_display = ('proyecto_e','revision')
    search_fields = ('proyecto_e__codigo', )
    autocomplete_fields = ['proyecto_e',]

@admin.register(Proyecto_E_SIA)
class Proyecto_E_SIA_Admin(ImportExportModelAdmin):
    resource_class = Proyecto_E_SIA_Resource
    list_display = ('proyecto_e', 'sia')
    search_fields = ('proyecto_e__codigo', 'sia__CodProyecto')
    autocomplete_fields = ['proyecto_e', 'sia']


