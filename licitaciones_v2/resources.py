from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import CategoryLicitacion, Licitacion, Propuesta, PropuestaDetalle


class CategoryLicitacionResource(resources.ModelResource):
    class Meta:
        model = CategoryLicitacion
        fields = ("nombre_categoria",)
        import_id_fields = ["nombre_categoria"]
        skip_unchanged = True
        report_skipped = True


class LicitacionResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(CategoryLicitacion, 'nombre_categoria'),
    )

    class Meta:
        model = Licitacion
        fields = (
            "rfq",
            "category",
            "rfq_type",
            "creation_date",
            "publication_date",
            "closed_date",
            "closed_hour",
            "estado_lic",
            "gral_desc",
            "proc_area",
        )
        import_id_fields = ["rfq"]
        skip_unchanged = True
        report_skipped = True
        # Bulk import: agrupa INSERT/UPDATE en batches con bulk_create/bulk_update.
        # Sin esto, django-import-export hace un save() por fila (28k saves)
        # y termina en timeout de conexion Postgres.
        use_bulk = True
        batch_size = 1000


class PropuestaResource(resources.ModelResource):
    rfq = fields.Field(
        column_name='rfq',
        attribute='rfq',
        widget=ForeignKeyWidget(Licitacion, 'rfq'),
    )
    fecha_primer_registro = fields.Field(
        column_name='fecha_primer_registro',
        attribute='fecha_primer_registro',
        readonly=True,
    )
    fecha_ultima_actualizacion = fields.Field(
        column_name='fecha_ultima_actualizacion',
        attribute='fecha_ultima_actualizacion',
        readonly=True,
    )
    totalmonto = fields.Field(
        column_name='totalmonto',
        attribute='totalmonto',
        readonly=True,
    )

    class Meta:
        model = Propuesta
        fields = (
            "bid",
            "rfq",
            "bid_proponente",
            "bid_vendor_name",
            "bid_date",
            "bid_status",
            "resultado",
            "fecha_primer_registro",
            "fecha_ultima_actualizacion",
            "totalmonto",
        )
        import_id_fields = ["bid"]
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        batch_size = 1000


class PropuestaDetalleResource(resources.ModelResource):
    bid = fields.Field(
        column_name='bid',
        attribute='bid',
        widget=ForeignKeyWidget(Propuesta, 'bid'),
    )
    fecha_ultima_actualizacion = fields.Field(
        column_name='fecha_ultima_actualizacion',
        attribute='fecha_ultima_actualizacion',
        readonly=True,
    )

    class Meta:
        model = PropuestaDetalle
        fields = (
            "bid",
            "bid_line_no",
            "bid_line_amount",
            "bid_line_number",
            "bid_line_price",
            "quantity",
            "fecha_ultima_actualizacion",
        )
        import_id_fields = ["bid", "bid_line_no"]
        skip_unchanged = True
        report_skipped = True
        # Con 528k filas, use_bulk es imprescindible — sin esto el sync
        # timeout-ea la conexion Postgres alrededor de los 65 minutos.
        use_bulk = True
        batch_size = 2000
