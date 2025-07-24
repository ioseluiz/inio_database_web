from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import Contrato_Resource

from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(ImportExportModelAdmin):
    resource_class = Contrato_Resource
    list_display = ('numero_contrato','description','rubro','tipo_licitacion','numero_licitacion',
                    'numero_propuesta_ganadora',
                    'status','fecha_adjudicacion','fiscal_year','fiscal_month','vendor_name',
                    'monto_contrato_original', 'monto_pagado','fecha_promesa','fecha_maxima_entrega')
    search_fields =('numero_contrato','description','numero_licitacion')
