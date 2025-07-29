from django.contrib import admin

# Register your models here.
from .models import Licitacion, CategoryLicitacion, Propuesta, Enmienda

admin.site.register(Licitacion)
admin.site.register(CategoryLicitacion)
admin.site.register(Propuesta)
admin.site.register(Enmienda)