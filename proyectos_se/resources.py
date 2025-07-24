from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_SE

class Proyecto_SE_Resource(resources.ModelResource):
    class Meta:
        model = Proyecto_SE
        fields = (
            "codigo",
            "title",
            "fecha_entrada",
            "fecha_salida",
            "fecha_sol_fondos_aprob",
            "fecha_sol_fondos_aprob",
            "comentarios",
            "status",
        )
        import_id_fields = ['codigo']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons