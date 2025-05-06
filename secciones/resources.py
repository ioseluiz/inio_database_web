from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Seccion

class SeccionResource(resources.ModelResource):
    class Meta:
        model = Seccion
        fields = (
            "name",
            "is_active",

        )
        import_id_fields = ['name']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons