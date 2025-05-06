from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin


from .models import Proyecto_C_Estimador
from .resources import Proyecto_CC_EstimadorResource


@admin.register(Proyecto_C_Estimador)
class Proyecto_CC_EstimadorAdmin(ImportExportActionModelAdmin):
    resource_class=Proyecto_CC_EstimadorResource
    list_display = ("proyecto_c", "estimador")
    autocomplete_fields = ['proyecto_c','estimador']