from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_CC

class Proyecto_CC_Resource(resources.ModelResource):
    class Meta:
        model = Proyecto_CC
        fields = (
            "codigo",
            "title",
            "seccion",
            "coordinador",
            "fecha_entrada",
            "fecha_envio_FIO",
            "fecha_sol_fondos_aprob",
            "fecha_recibo_fondos_aprob",
            "comentarios",
            "estado",
            "asignacion_presup_final",
            "precio_acp"

        )
        import_id_fields = ['codigo']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons