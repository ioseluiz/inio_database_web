from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Licitacion, CategoryLicitacion, Propuesta, Enmienda

from .resources import LicitacionResource, PropuestaResource


@admin.register(Licitacion)
class LicitacionAdmin(ImportExportModelAdmin):
    """
    Registra el modelo Licitacion en el sitio de administración.
    """
    resource_class = LicitacionResource
    # Esta es la línea clave que solucionará el error.
    # Se basa en el campo 'rfq' que usas en otros lugares.
    search_fields = ['rfq']

    # También puedes agregar otros campos para mejorar la visualización en el admin.
    list_display = ('rfq', 'gral_desc', 'publication_date') # Ejemplo: ajusta los campos según tu modelo
    # list_filter = ('estado',) # Ejemplo

@admin.register(Enmienda)
class EnmiendaAdmin(admin.ModelAdmin):
    """
    Registra el modelo Enmienda en el sitio de administracion.
    """
    search_fields = ['licitacion__rfq']
    list_display = ('enmienda_id','licitacion', 'fecha_enmienda','enmienda_desc')

@admin.register(Propuesta)
class PropuestaAdmin(ImportExportModelAdmin):
    """ 
    Registra el modelo Propuesta en el sitio de administracion.
    """
    resource_class = PropuestaResource
    search_fields = ['licitacion__rfq']
    list_display = ('licitacion','bid_vendor_name', 'bid_line_amount','bid_status')