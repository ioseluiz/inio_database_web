from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_E, HorasApoyo, Proyecto_E_SIA
from SIA.models import tblProyectos

class Proyecto_E_Resource(resources.ModelResource):
    class Meta:
        model = Proyecto_E
        fields = (
            "codigo",
            "title",
            "fecha_entrada",
            "fecha_salida",
            "seccion",
            "coordinador",
            "bldg",
            "comentarios",
            "fiscal_year",
            "asignacion_presup",

        )
        import_id_fields = ['codigo']

        # --- Important settings for import behaviour ---
        skip_unchanged = True # If True, rows that have not changed won't be updated
        report_skipped = True # If True, reports skipped rows and reasons

class HorasApoyo_Resource(resources.ModelResource):
    proyecto_e = fields.Field(
        column_name='proyecto_e',
        attribute='proyecto_e',
        widget=ForeignKeyWidget(Proyecto_E, 'codigo')
    )
    class Meta:
        model = HorasApoyo
        
        fields = (
            "proyecto_e",
            "revision",
            "hr_diseno_inic_ar",
            "hr_diseno_inic_ic",
            "hr_diseno_inic_ie",
            "hr_diseno_inic_ih",
            "hr_diseno_inie_dm",
            "hr_diseno_inie_ee",
            "hr_diseno_inie_sm",
            "hr_diseno_inig_ig",
            "hr_diseno_inig_pe",
            "hr_diseno_inio_ce",
            "hr_diseno_inio_es",
            "hr_diseno_init",

            "hr_apoyo_inic_ar",
            "hr_apoyo_inic_ic",
            "hr_apoyo_inic_ie",
            "hr_apoyo_inic_ih",
            "hr_apoyo_inie_dm",
            "hr_apoyo_inie_ee",
            "hr_apoyo_inie_sm",
            "hr_apoyo_inig_ig",
            "hr_apoyo_inig_pe",
            "hr_apoyo_inio_ce",
            "hr_apoyo_inio_es",
            "hr_apoyo_init",
            
        )

        skip_unchanged = True
        report_skipped = True


    def import_row(self, row, instance_loader, **kwargs):
        # Intentamos buscar el código en la base de datos
        codigo_proyecto = row.get('proyecto_e')
        exists = Proyecto_E.objects.filter(codigo=codigo_proyecto).exists()
        
        if not exists:
            return super().import_row(row, instance_loader, **kwargs) # Esto fallará
            # Pero para saltarlo de forma segura:
            return None # Retornar None indica que no se debe procesar la fila

    def skip_row(self, instance, original, row, import_validation_errors=None):
        # Si el proyecto_e no se asignó (es None), saltamos la fila
        if not instance.proyecto_e_id:
            return True
        return super().skip_row(instance, original, row, import_validation_errors)


class Proyecto_E_SIA_Resource(resources.ModelResource):

    proyecto_e = fields.Field(
        column_name='proyecto_e',
        attribute='proyecto_e',
        widget=ForeignKeyWidget(Proyecto_E, 'codigo')
    )

    sia = fields.Field(
        column_name='sia',
        attribute='sia',
        widget=ForeignKeyWidget(tblProyectos, 'codigo')
    )

    class Meta:
        model = Proyecto_E_SIA
        import_id_fields = ['proyecto_e', 'sia']

        fields = ('proyecto_e', 'sia')

        skip_unchanged = True
        report_skipped = True
