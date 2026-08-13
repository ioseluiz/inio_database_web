"""
LoginRequiredMiddleware
=======================

Cierra por defecto todo el sitio: cualquier request de un usuario no
autenticado se redirige al login. Se listan explicitamente los prefijos de
URL exentos: pantalla de login/logout, endpoints con auth por token, admin
(que tiene su propio flujo de login), assets estaticos y el reload dev.

Motivacion: por historia solo la vista raiz tenia @login_required. El resto
de las 28 vistas de negocio (proyectos, licitaciones, contratos, etc.)
estaban abiertas al mundo. Este middleware cierra el gap sin exigir tocar
cada vista.

Para excluir una nueva ruta, agregarla a EXEMPT_PREFIXES. Priorizar
prefijos especificos sobre '/' generales.
"""

from django.http import HttpResponseRedirect
from django.urls import reverse


EXEMPT_PREFIXES = (
    "/user/sign-in",
    "/user/sign-out",
    "/static/",
    "/media/",
    # Endpoints de solo lectura autenticados via Authorization: Token <valor>
    # (ver proyectos_C/api_dashboard.py). Consumidos por el pipeline ETL local.
    "/proyectosc/api/dashboard/",
    # El admin de Django tiene su propio flujo de autenticacion (login,
    # session, permisos por is_staff/is_superuser). Lo dejamos manejar solo.
    # Path movido a /inio-admin/ para reducir ruido en logs y superficie de
    # ataque contra el default /admin/.
    "/inio-admin/",
    # Solo activo con DEBUG=True; en produccion no responde nada.
    "/__reload__/",
)


class LoginRequiredMiddleware:
    """Middleware que exige sesion autenticada excepto para EXEMPT_PREFIXES."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path
            if not any(path.startswith(prefix) for prefix in EXEMPT_PREFIXES):
                login_url = reverse("accounts:sign-in")
                return HttpResponseRedirect(f"{login_url}?next={request.path}")
        return self.get_response(request)
