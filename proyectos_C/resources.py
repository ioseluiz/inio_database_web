from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Proyecto_CC, Proyecto_CC_Estimado_Conceptual, Proyecto_CC_Licitacion, Proyecto_CC_SIA, Proyecto_CC_Secciones_MF
from proyectos_E.models import Proyecto_E
from licitaciones.models import Licitacion
from SIA.models import tblProyectos

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


class Proyecto_CC_Licitacion_Resource(resources.ModelResource):

    proyecto_cc = fields.Field(
        column_name='proyecto_cc',
        attribute='proyecto_cc',
        widget=ForeignKeyWidget(Proyecto_CC, 'codigo')
    )

    licitacion = fields.Field(
        column_name='licitacion',
        attribute='licitacion',
        widget=ForeignKeyWidget(Licitacion, 'rfq')
    )

    class Meta:
        model = Proyecto_CC_Licitacion
        import_id_fields = ['proyecto_cc', 'licitacion']

        fields = ('proyecto_cc', 'licitacion')

        skip_unchanged = True
        report_skipped = True

class Proyecto_CC_SIA_Resource(resources.ModelResource):
    proyecto_cc = fields.Field(
        column_name='proyecto_cc',
        attribute='proyecto_cc',
        widget=ForeignKeyWidget(Proyecto_CC, 'codigo')
    )
    sia = fields.Field(column_name='sia',
                       attribute='sia',
                       widget=ForeignKeyWidget(tblProyectos, 'CodProyecto'))
    
    class Meta:
        model = Proyecto_CC_SIA
        import_id_fields = ['proyecto_cc', 'sia']
        fields = ('proyecto_cc', 'sia')

        skip_unchanged = True
        report_skipped = True
    
class Proyecto_CC_Secciones_MF_Resource(resources.ModelResource):
    proyecto_cc = fields.Field(
        column_name='proyecto_cc',
        attribute='proyecto_cc',
        widget=ForeignKeyWidget(Proyecto_CC, 'codigo')
    )

    class Meta:
        model = Proyecto_CC_Secciones_MF
        import_id_fields = ['proyecto_cc', 'seccion']

        fields = ('proyecto_cc', 'division', 'seccion', 'descripcion')

        skip_unchanged = True
        report_skipped = True

    def skip_row(self, instance, original, row, import_validation_errors=None):
            codigo = row.get('proyecto_cc')

            if not codigo:
                return True
            
            # 3. VERIFICACIÓN CLAVE: Si el proyecto NO existe en la BD, saltamos la línea.
            # Esto evita el "Internal Server Error"
            if not Proyecto_CC.objects.filter(codigo=codigo).exists():
                return True # True significa "SÍ, SALTA ESTA LÍNEA"

            return super().skip_row(instance, original, row, import_validation_errors)

