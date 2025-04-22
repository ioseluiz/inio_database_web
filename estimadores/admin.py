from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import EstimadorResource

from .models import Estimador

@admin.register(Estimador)
class EstimadorAdmin(ImportExportModelAdmin):
    resource_class = EstimadorResource
    list_display = ('name', 'initials','is_active')
    search_fields = ('name', 'initials')
