from django.apps import AppConfig


class LicitacionesV2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'licitaciones_v2'

    def ready(self):
        from . import signals  # noqa: F401
