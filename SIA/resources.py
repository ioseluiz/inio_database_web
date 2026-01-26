from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import tblProyectos, tblTransacciones

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


class tblTransacciones_Resource(resources.ModelResource):
    class Meta:
        model = tblTransacciones
        fields = (
            "Fecha",
            "IP",
            "CodProyecto",
            "HoraRegular",
            "HoraExtra",
            "HoraComp",
            "CodRamo"
        )

        import_id_fields = ('Fecha', 'IP', 'CodProyecto')

        # -- Important settings for import behaviour ---
        skip_unchanged = True
        report_skipped = True

    def skip_row(self, instance, original, row, import_validation_errors=None):
        """
        Verifica si el CodProyecto del CSV existe en la base de datos.
        Si no existe, salta la línea (retorna True).
        """
        cod_proyecto_csv = row.get('CodProyecto')
        
        # Si el campo viene vacío, saltamos
        if not cod_proyecto_csv:
            return True

        # Verificamos si existe en la tabla tblProyectos
        if not tblProyectos.objects.filter(CodProyecto=cod_proyecto_csv).exists():
            # Opcional: Imprimir en consola para saber qué se saltó
            print(f"Saltando fila: Proyecto {cod_proyecto_csv} no encontrado.")
            return True
            
        return super().skip_row(instance, original, row, import_validation_errors)