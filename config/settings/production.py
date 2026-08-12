from .base import *
import os


if not DEBUG:
    allowed_hosts_string = os.getenv('ALLOWED_HOSTS')

    # Convierte la cadena en una lista, separando por las comas.
    # Si la variable no esta definida, devuelve una lista vacia para evitar errores.
    ALLOWED_HOSTS = allowed_hosts_string.split(',') if allowed_hosts_string else []

    # HTTPS/TLS ya provisto por Nginx delante de Gunicorn via unix socket.
    # Nginx debe pasar el header X-Forwarded-Proto=https en cada request (esta
    # incluido en el snippet estandar /etc/nginx/proxy_params de Ubuntu).
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Fuerza HTTPS a nivel Django (redirect adicional a la que ya hace Nginx).
    SECURE_SSL_REDIRECT = True

    # Cookies solo por HTTPS.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS: el navegador recuerda usar HTTPS para futuros requests.
    # 1 ano ya que HTTPS quedo estable con Let's Encrypt (renovacion automatica).
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # PRELOAD solo si se compromete a mantener HTTPS permanentemente. Dejar en
    # False hasta que la operacion este consolidada por varios meses.
    SECURE_HSTS_PRELOAD = False

    # Cabeceras defensivas adicionales.
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    X_FRAME_OPTIONS = 'DENY'

    # CSRF: confiar en el hostname sslip.io + IP publica para POSTs sobre HTTPS.
    CSRF_TRUSTED_ORIGINS = [
        'https://20-81-211-62.sslip.io',
        'https://20.81.211.62',
    ]
