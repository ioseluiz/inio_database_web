from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_CC, Proyecto_CC_Estimado_Conceptual
from proyectos_E.models import Proyecto_E

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

class Proyecto_CC_Estimado_Conceptal_Resource(resources.ModelResource):

    proyecto_cc = fields.Field(
        column_name='proyecto_cc',
        attribute='proyecto_cc',
        widget=ForeignKeyWidget(Proyecto_CC, 'codigo')
    )

    estimado_conceptual = fields.Field(
        column_name='estimado_conceptual',
        attribute='estimado_conceptual',
        widget=ForeignKeyWidget(Proyecto_E, 'codigo')
    )

    class Meta:
        model = Proyecto_CC_Estimado_Conceptual
        import_id_fields = ['proyecto_cc', 'estimado_conceptual']

        fields = ('proyecto_cc', 'estimado_conceptual')

        skip_unchanged = True
        report_skipped = True
