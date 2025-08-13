from .base import *
import os


if not DEBUG:
    allowed_hosts_string = os.getenv('ALLOWED_HOSTS')
    
    # Convierte la cadena en una lista, separando por las comas.
    # Si la variable no está definida, devuelve una lista vacía para evitar errores.
    ALLOWED_HOSTS = allowed_hosts_string.split(',') if allowed_hosts_string else []
    # SECURE_SSL_REDIRECT = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    # SECURE_HSTS_SECONDS = 31536000 # 1 año
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    # print(ALLOWED_HOSTS)