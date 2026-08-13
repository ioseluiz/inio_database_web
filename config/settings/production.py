from .base import *
import os


if not DEBUG:
    # Logging de eventos de seguridad (OWASP A09).
    # Rota archivos a 10 MB manteniendo 5 backups (~50 MB por logger).
    # Los archivos viven en BASE_DIR/logs/ (owned por iniodeploy, gitignored).
    LOG_DIR = BASE_DIR / 'logs'
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'security': {
                'format': '{asctime} {levelname} {name} {process:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'security_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(LOG_DIR / 'security.log'),
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'security',
            },
            'request_file': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(LOG_DIR / 'requests.log'),
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'security',
            },
        },
        'loggers': {
            # DisallowedHost, InvalidHostFound, CSRF failures, etc.
            'django.security': {
                'handlers': ['security_file'],
                'level': 'INFO',
                'propagate': False,
            },
            # Errores 4xx/5xx generados por vistas.
            'django.request': {
                'handlers': ['request_file'],
                'level': 'WARNING',
                'propagate': False,
            },
            # Intentos fallidos de login y bloqueos (django-axes).
            'axes': {
                'handlers': ['security_file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

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

    # SameSite explicito (coincide con el default de Django 'Lax' pero mejor no
    # depender del default por si cambia). 'Lax' permite navegacion top-level
    # entrante desde links externos (email, chat) sin perder la sesion.
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

    # Ciclo de vida de la sesion (OWASP A07).
    # - AGE = 12h: maximo absoluto de sesion desde ultima actividad (con
    #   SAVE_EVERY_REQUEST=True la sesion se refresca en cada interaccion).
    # - EXPIRE_AT_BROWSER_CLOSE: la cookie no tiene expiracion explicita en el
    #   navegador -> muere al cerrar el navegador. Server-side sigue vigente
    #   el limite de 12h que impone AGE.
    # - SAVE_EVERY_REQUEST: cada request refresca el timestamp de la sesion,
    #   implementando idle timeout: 12h sin actividad = logout automatico.
    SESSION_COOKIE_AGE = 43200
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SAVE_EVERY_REQUEST = True

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

    # Content Security Policy (OWASP A05).
    # Restringe de donde el navegador puede cargar recursos: cualquier <script>,
    # <style>, <img>, fetch/XHR, iframe, etc. desde origenes distintos a los
    # listados se bloquea. Mitiga XSS incluso si un atacante inyecta contenido.
    #
    # 'unsafe-inline' en script-src y style-src se mantiene porque:
    #   - Django admin renderiza <script> y <style> inline en sus templates
    #   - Tailwind + HTMX del sitio usan algunos inline styles
    # Endurecer a nonces requiere modificar templates del admin (fase futura).
    #
    # CDNs permitidos (usados por los templates actuales):
    #   - cdnjs.cloudflare.com : Font Awesome (iconos del home y otras vistas)
    #   - cdn.jsdelivr.net     : Tom Select, Frappe Gantt en proyectos_c
    # Mudarlos a self-hosted es hardening futuro (menos superficie externa).
    CONTENT_SECURITY_POLICY = {
        'DIRECTIVES': {
            'default-src': ["'self'"],
            'script-src': [
                "'self'",
                "'unsafe-inline'",
                'https://cdn.jsdelivr.net',
            ],
            'style-src': [
                "'self'",
                "'unsafe-inline'",
                'https://cdnjs.cloudflare.com',
                'https://cdn.jsdelivr.net',
            ],
            'img-src': ["'self'", 'data:'],
            'font-src': [
                "'self'",
                'https://cdnjs.cloudflare.com',
            ],
            'connect-src': ["'self'"],
            # Bloquea embed en iframes externos (equivalente a X-Frame-Options DENY).
            'frame-ancestors': ["'none'"],
            'base-uri': ["'self'"],
            'form-action': ["'self'"],
            # Fuerza al navegador a cargar recursos http:// como https://.
            'upgrade-insecure-requests': True,
        },
    }
