from django.contrib import admin


from .models import Proyecto_E_Estimador

from proyectos_E.models import Proyecto_E
from estimadores.models import Estimador


@admin.register(Proyecto_E_Estimador)
class Proyecto_E_EstimadorAdmin(admin.ModelAdmin):
    list_display = ("proyecto_e", "estimador")
    autocomplete_fields = ['proyecto_e','estimador']

