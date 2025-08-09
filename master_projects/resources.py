from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import MasterProject
from proyectos_C.models import Proyecto_CC

class Master_Proyecto_Resource(resources.ModelResource):
    proyecto_cc = fields.Field(
        column_name='proyecto_cc',
        attribute='proyecto_cc',
        widget=ForeignKeyWidget(Proyecto_CC, 'codigo')
    )
     
    class Meta:

        model = MasterProject
        fields = (
            "unidad_solicitante",
            "nip",
            "proyecto_cc",
            "fecha_estimada_entrega_owner",
            "fiscal_year",
            "comentarios",
            "estado",
        )
        import_id_fields = ['proyecto_cc']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons