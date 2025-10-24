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
            "hr_diseno_inie_ig",
            "hr_diseno_inie_pe",
            "hr_diseno_inie_ce",
            "hr_diseno_inie_es",
            "hr_diseno_init",

            "hr_apoyo_inic_ar",
            "hr_apoyo_inic_ic",
            "hr_apoyo_inic_ie",
            "hr_apoyo_inic_ih",
            "hr_apoyo_inie_dm",
            "hr_apoyo_inie_ee",
            "hr_apoyo_inie_sm",
            "hr_apoyo_inie_ig",
            "hr_apoyo_inie_pe",
            "hr_apoyo_inie_ce",
            "hr_apoyo_inie_es",
            "hr_apoyo_init",
            
        )

        skip_unchanged = True
        report_skipped = True


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
