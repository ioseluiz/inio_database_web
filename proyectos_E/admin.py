from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_E_Resource

from .models import Proyecto_E

@admin.register(Proyecto_E)
class Proyecto_EAdmin(ImportExportModelAdmin):
    resource_class = Proyecto_E_Resource
    list_display = ('codigo','title','fecha_entrada','fecha_salida','seccion','coordinador','bldg')
    search_fields =('codigo','title')
