from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import tblProyectos

class tblProyectos_Resource(resources.ModelResource):
    class Meta:
        model = tblProyectos
        fields = (
            "CodProyecto",
            "NomProyecto",
            "CodCuenta",
            "CodRamo",
            "CodCliente",
            "Prioridad",
            "TipoCosto",
            "Fiscal",
            "DescProyecto",
            "FechaRec",
            "FechaIni",
            "FechaEIES",
            "FechaEst",
            "FechaReal",
            "IPCoordinador",
            "Abierto"

        )
        import_id_fields = ['CodProyecto']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons