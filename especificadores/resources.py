from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Especificador

class EspecificadorResource(resources.ModelResource):
    class Meta:
        model = Especificador
        fields = (
            "nombre",
            "iniciales",
            "is_active",

        )
        import_id_fields = ['iniciales']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons