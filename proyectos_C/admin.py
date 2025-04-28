from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_CC_Resource

from .models import Proyecto_CC

@admin.register(Proyecto_CC)
class Proyecto_CCAdmin(ImportExportModelAdmin):
    resource_class = Proyecto_CC_Resource
    list_display = ('codigo','title','fecha_entrada','fecha_envio_FIO','seccion','coordinador','estado','asignacion_presup_final','precio_acp')
    search_fields =('codigo','title')
