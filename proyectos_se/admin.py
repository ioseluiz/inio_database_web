from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Proyecto_SE_Resource

from .models import Proyecto_SE

@admin.register(Proyecto_SE)
class Proyecto_CCAdmin(ImportExportModelAdmin):
    resource_class = Proyecto_SE_Resource
    list_display = ('codigo','title','fecha_entrada','fecha_salida','fecha_sol_fondos','fecha_sol_fondos_aprobados','comentarios','status')
    search_fields =('codigo','title')
