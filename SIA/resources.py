from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateTimeWidget

from .models import tblProyectos, tblTransacciones

class SoftForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        try:
            return super().clean(value, row, **kwargs)
        except self.model.DoesNotExist:
            # Si no existe, devolvemos None en lugar de lanzar error.
            # Esto permite que el proceso continúe y 'skip_row' haga su trabajo.
            return None

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
    # Campos con widgets personalizados
    Fecha = fields.Field(
        attribute='Fecha',
        column_name='Fecha',
        widget=DateTimeWidget(format='%m/%d/%Y %H:%M')
    )

    # --- 2. Usamos el Widget "Suave" aquí ---
    CodProyecto = fields.Field(
        attribute='CodProyecto',
        column_name='CodProyecto',
        # Usamos SoftForeignKeyWidget en lugar del estándar
        widget=SoftForeignKeyWidget(tblProyectos, field='CodProyecto')
    )

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
        skip_unchanged = True
        report_skipped = True

    # --- 3. Método para saltar filas (Igual que antes) ---
    def skip_row(self, instance, original, row, import_validation_errors=None):
        cod_proyecto_csv = row.get('CodProyecto')
        
        if not cod_proyecto_csv:
            return True

        # Verificamos manualmente si existe. Si no, SALTAMOS la fila.
        if not tblProyectos.objects.filter(CodProyecto=cod_proyecto_csv).exists():
            return True
            
        return super().skip_row(instance, original, row, import_validation_errors)