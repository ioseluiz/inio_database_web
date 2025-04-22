from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_E

class Proyecto_E_Resource(resources.ModelResource):
    class Meta:
        model = Proyecto_E
        fields = (
            "codigo",
            "title",
            "fecha_entrada",
            "fecha_salida",
            "seccion",
            "coordinador",
            "bldg",
            "comentarios",
            "fiscal_year"

        )

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons
