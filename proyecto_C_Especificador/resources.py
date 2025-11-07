from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_C_Especificador
from especificadores.models import Especificador
from proyectos_C.models import Proyecto_CC



class Proyecto_CC_EspecificadorResource(resources.ModelResource):
    proyecto_cc = Field(
        column_name="proyecto_cc",
        attribute="proyecto_cc",
        widget=ForeignKeyWidget(Proyecto_CC, field="codigo")
    )
    especificador = Field(
        column_name="especificador",
        attribute="especificador",
        widget=ForeignKeyWidget(Especificador, field="iniciales")
    )

    class Meta:
        model = Proyecto_C_Especificador
        fields = ("proyecto_cc","especificador")
        import_id_fields =["proyecto_cc","especificador"]

        # --- Important settings for import behaviour ---
        skip_unchanged = True  # If True, rows that have not changed won't be updated
        report_skipped = True  # If True, reports skipped rows and reasons