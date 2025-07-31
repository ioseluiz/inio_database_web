from django.contrib import admin

# Register your models here.
from .models import Licitacion, CategoryLicitacion, Propuesta, Enmienda

# admin.site.register(Licitacion)
admin.site.register(CategoryLicitacion)

admin.site.register(Enmienda)

@admin.register(Licitacion)
class LicitacionAdmin(admin.ModelAdmin):
    """
    Registra el modelo Licitacion en el sitio de administración.
    """
    # Esta es la línea clave que solucionará el error.
    # Se basa en el campo 'rfq' que usas en otros lugares.
    search_fields = ['rfq']

    # También puedes agregar otros campos para mejorar la visualización en el admin.
    list_display = ('rfq', 'gral_desc', 'publication_date') # Ejemplo: ajusta los campos según tu modelo
    # list_filter = ('estado',) # Ejemplo

@admin.register(Propuesta)
class PropuestaAdmin(admin.ModelAdmin):
    """ 
    Registra el modelo Propuesta en el sitio de administracion.
    """
    search_fields = ['licitacion__rfq']
    list_display = ('licitacion','bid_vendor_name', 'bid_line_amount','bid_status')