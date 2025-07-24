from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import SIA_Resource

from .models import SIA

@admin.register(SIA)
class SIAAdmin(ImportExportModelAdmin):
    resource_class = SIA_Resource
    list_display = ('CodProyecto','NomProyecto','CodCuenta','CodRamo','CodCliente','Prioridad','TipoCosto','Fiscal','DescProyecto',
                    'FechaRec', 'FechaIni','FechaEIES','FechaEst','FechaReal','IPCoordinador','Abierto')
    search_fields =('CodProyecto','NomProyecto')
