from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget
from datetime import datetime
from .models import tblProyectos, tblTransacciones

# --- 1. Widget de Fecha "Todo Terreno" ---
class FlexibleDateTimeWidget(widgets.Widget):
    """
    Intenta leer la fecha usando múltiples formatos posibles.
    Soporta:
    1. 2026-01-22 00:00:00 (Formato que indicaste)
    2. 1/23/2026 0:00      (Formato en tu archivo CSV actual)
    """
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        
        value = str(value).strip()
        
        # Lista de formatos a probar, en orden de prioridad
        formats_to_try = [
            '%Y-%m-%d %H:%M:%S',  # Ej: 2026-01-22 00:00:00
            '%Y-%m-%d %H:%M',     # Ej: 2026-01-22 00:00
            '%m/%d/%Y %H:%M',     # Ej: 1/23/2026 0:00 (Mes/Día/Año)
            '%d/%m/%Y %H:%M',     # Ej: 23/01/2026 0:00 (Día/Mes/Año)
        ]

        for fmt in formats_to_try:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        # Si fallan los formatos estándar, intentamos el método manual
        # para casos difíciles (ej: fechas sin ceros como 1/1/2026)
        try:
            parts = value.split(' ')
            date_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else "00:00"

            # Detectamos si usa '/' o '-'
            separator = '/' if '/' in date_part else '-'
            date_components = list(map(int, date_part.split(separator)))
            
            # Asumimos orden Mes/Día/Año si usa '/' (formato USA)
            if separator == '/':
                month, day, year = date_components
            else:
                # Asumimos Año-Mes-Día si usa '-'
                year, month, day = date_components

            time_components = list(map(int, time_part.split(':')))
            hour = time_components[0]
            minute = time_components[1] if len(time_components) > 1 else 0
            second = time_components[2] if len(time_components) > 2 else 0

            return datetime(year, month, day, hour, minute, second)
        except Exception:
            raise ValueError(f"No se pudo leer la fecha: {value}")

# --- 2. Widget de Llave Foránea "Suave" ---
class SoftForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        try:
            return super().clean(value, row, **kwargs)
        except self.model.DoesNotExist:
            return None

# --- RECURSOS ---

class tblProyectos_Resource(resources.ModelResource):
    class Meta:
        model = tblProyectos
        fields = (
            "CodProyecto", "NomProyecto", "CodCuenta", "CodRamo",
            "CodCliente", "Prioridad", "TipoCosto", "Fiscal",
            "DescProyecto", "FechaRec", "FechaIni", "FechaEIES",
            "FechaEst", "FechaReal", "IPCoordinador", "Abierto"
        )
        import_id_fields = ['CodProyecto']
        skip_unchanged = True
        report_skipped = True

class tblTransacciones_Resource(resources.ModelResource):
    # Usamos nuestro widget flexible actualizado
    Fecha = fields.Field(
        attribute='Fecha',
        column_name='Fecha',
        widget=FlexibleDateTimeWidget()
    )

    # Usamos el widget suave para el proyecto
    CodProyecto = fields.Field(
        attribute='CodProyecto',
        column_name='CodProyecto',
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

    def skip_row(self, instance, original, row, import_validation_errors=None):
        cod_proyecto_csv = row.get('CodProyecto')
        
        if not cod_proyecto_csv:
            return True

        if not tblProyectos.objects.filter(CodProyecto=cod_proyecto_csv).exists():
            return True
            
        return super().skip_row(instance, original, row, import_validation_errors)