from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import tblProyectos_Resource

from .models import tblProyectos

# admin.site.register(tblProyectos)

@admin.register(tblProyectos)
class SIAAdmin(ImportExportModelAdmin):
    resource_class = tblProyectos_Resource
    list_display = ('CodProyecto','NomProyecto','CodCuenta','CodRamo','CodCliente','Prioridad','TipoCosto','Fiscal','DescProyecto',
                    'FechaRec', 'FechaIni','FechaEIES','FechaEst','FechaReal','IPCoordinador','Abierto')
    search_fields =('CodProyecto','NomProyecto')
