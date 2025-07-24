from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin


from .models import Proyecto_C_Especificador
from .resources import Proyecto_CC_EspecificadorResource


@admin.register(Proyecto_C_Especificador)
class Proyecto_CC_EspecificadorAdmin(ImportExportActionModelAdmin):
    resource_class=Proyecto_CC_EspecificadorResource
    list_display = ("proyecto_cc", "especificador")
    autocomplete_fields = ['proyecto_cc','especificador']