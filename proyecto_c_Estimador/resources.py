from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_C_Estimador
from estimadores.models import Estimador
from proyectos_C.models import Proyecto_CC

class Proyecto_CC_EstimadorResource(resources.ModelResource):
    proyecto_c = Field(
        column_name="proyecto_c",
        attribute="proyecto_c",
        widget=ForeignKeyWidget(Proyecto_CC, field="codigo")
    )
    estimador = Field(
        column_name="estimador",
        attribute="estimador",
        widget=ForeignKeyWidget(Estimador, field="initials")
    )

    class Meta:
        model = Proyecto_C_Estimador
        fields = ("proyecto_c","estimador")
        import_id_fields =["proyecto_c","estimador"]

         # --- Important settings for import behaviour ---
        skip_unchanged = True  # If True, rows that have not changed won't be updated
        report_skipped = True  # If True, reports skipped rows and reasons
        