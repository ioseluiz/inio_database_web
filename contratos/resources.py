from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Contrato




class Contrato_Resource(resources.ModelResource):
    class Meta:
        model = Contrato
        fields = (
            "numero_contrato",
            "description",
            "rubro",
            "tipo_licitacion",
            "numero_licitacion",
            "numero_propuesta_ganadora",
            "status",
            "fecha_cierre",
            "fecha_adjudicacion",
            "fiscal_year",
            "fiscal_month",
            "vendor_name",
            "monto_contrato_original",
            "monto_pagado",
            "fecha_promesa",
            "fecha_maxima_entrega"

        )
        import_id_fields = ['numero_contrato']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons