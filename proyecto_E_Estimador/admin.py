from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin


from .models import Proyecto_E_Estimador
from .resources import Proyecto_E_EstimadorResource


@admin.register(Proyecto_E_Estimador)
class Proyecto_E_EstimadorAdmin(ImportExportActionModelAdmin):
    resource_class=Proyecto_E_EstimadorResource
    list_display = ("proyecto_e", "estimador")
    autocomplete_fields = ['proyecto_e','estimador']

