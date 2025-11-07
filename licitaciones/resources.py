from import_export import resources, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Licitacion, CategoryLicitacion, Propuesta

class LicitacionResource(resources.ModelResource):

    catergory = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(CategoryLicitacion, 'nombre_categoria')
    )
    class Meta:
        model = Licitacion
        fields = ("rfq","category",
                  "rfq_type", "creation_date", "publication_date",
                  "closed_date", "closed_hour", "estado_lic", "gral_desc",
                  "proc_area")
        
        import_id_fields = ["rfq"]

        # --- Important settings for import behaviour ---
        skip_unchanged = True  # If True, rows that have not changed won't be updated
        report_skipped = True  # If True, reports skipped rows and reasons

class PropuestaResource(resources.ModelResource):
    licitacion = fields.Field(
        column_name='licitacion',
        attribute='licitacion',
        widget=ForeignKeyWidget(Licitacion, 'rfq')

    )
    class Meta:
        model = Propuesta
        fields = ("licitacion", "bid_proponente_id", "bid_line_amount", "bid_line_amount",
                    "bid_line_no", "bid_status", "bid_vendor_name","rfq_closed_date",
                    "rfq_closed_date", "rfq_method", "resultado")
        import_id_fields = ["licitacion"]

        # --- Important settings for import behaviour ---
        skip_unchanged = True  # If True, rows that have not changed won't be updated
        report_skipped = True  # If True, reports skipped rows and reasons