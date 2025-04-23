from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_E_Estimador
from estimadores.models import Estimador
from proyectos_E.models import Proyecto_E

class Proyecto_E_EstimadorResource(resources.ModelResource):
    proyecto_e = Field(
        column_name="proyecto_e",
        attribute="proyecto_e",
        widget=ForeignKeyWidget(Proyecto_E, field="codigo")
    )
    estimador = Field(
        column_name="estimador",
        attribute="estimador",
        widget=ForeignKeyWidget(Estimador, field="initials")
    )

    class Meta:
        model = Proyecto_E_Estimador
        fields = ("proyecto_e","estimador")
        import_id_fields =["proyecto_e","estimador"]

         # --- Important settings for import behaviour ---
        skip_unchanged = True  # If True, rows that have not changed won't be updated
        report_skipped = True  # If True, reports skipped rows and reasons
        