from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_SE_Resource

from .models import Proyecto_SE

@admin.register(Proyecto_SE)
class Proyecto_SEAdmin(ImportExportModelAdmin):
    resource_class = Proyecto_SE_Resource
    list_display = ('codigo','title','fecha_entrada','fecha_envio_FIO','seccion','coordinador','estado','asignacion_presup_final','precio_acp')
    search_fields =('codigo','title')
