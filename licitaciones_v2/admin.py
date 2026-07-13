from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import CategoryLicitacion, Licitacion, Propuesta, PropuestaDetalle
from .resources import (
    CategoryLicitacionResource,
    LicitacionResource,
    PropuestaResource,
    PropuestaDetalleResource,
)


@admin.register(CategoryLicitacion)
class CategoryLicitacionAdmin(ImportExportModelAdmin):
    resource_class = CategoryLicitacionResource
    search_fields = ('nombre_categoria',)
    list_display = ('nombre_categoria',)


@admin.register(Licitacion)
class LicitacionAdmin(ImportExportModelAdmin):
    resource_class = LicitacionResource
    search_fields = ('rfq', 'gral_desc')
    list_display = ('rfq', 'gral_desc', 'publication_date', 'estado_lic')
    list_filter = ('estado_lic', 'category')


@admin.register(Propuesta)
class PropuestaAdmin(ImportExportModelAdmin):
    resource_class = PropuestaResource
    search_fields = ('=bid', 'rfq__rfq', 'bid_vendor_name', 'bid_proponente')
    list_display = ('bid', 'rfq', 'bid_vendor_name', 'bid_status', 'totalmonto', 'bid_date')
    list_filter = ('bid_status',)
    raw_id_fields = ('rfq',)


@admin.register(PropuestaDetalle)
class PropuestaDetalleAdmin(ImportExportModelAdmin):
    resource_class = PropuestaDetalleResource
    search_fields = ('=bid__bid', 'bid__rfq__rfq')
    list_display = ('bid', 'bid_line_no', 'bid_line_amount', 'bid_line_price', 'quantity')
    raw_id_fields = ('bid',)
