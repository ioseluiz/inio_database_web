from .base import *

if DEBUG:
    ALLOWED_HOSTS = ['*']

    NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

    # Override para desarrollo local sin Postgres.
    # Produccion usa production.py y NO importa este override.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }