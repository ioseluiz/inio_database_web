from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Estimador

class EstimadorResource(resources.ModelResource):
    class Meta:
        model = Estimador
        fields = (
            "name",
            "initials",
            "is_active",

        )
        import_id_fields = ['initials']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons