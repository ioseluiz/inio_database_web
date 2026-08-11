"""Endpoints CSV que alimentan el dashboard local de índices de licitaciones.

Los consume el pipeline headless en `INICA/02_software/09_ordenar_licitaciones`
(script `descargar_proyectos_remoto.py`), que corre a diario en la máquina de
`jlmunoz` antes de ejecutar el ETL de licitaciones.

Auth: header `Authorization: Token <valor>`. El token vive en la env var
`DASHBOARD_EXPORT_TOKEN` (setear en `.env` de prod). Si no está configurada,
el endpoint responde 403 — nunca queda abierto por defecto.

El formato del CSV lo dictan los loaders locales
(`cargar_proyectos.py` y `cargar_proyecto_licitacion.py`); no cambiar sin
sincronizar allá.
"""
import csv
import os
import secrets as _secrets

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET

from .models import Proyecto_CC, Proyecto_CC_Licitacion


COLS_PROYECTOS = (
    "codigo", "title", "seccion", "coordinador",
    "fecha_entrada", "fecha_envio_FIO",
    "fecha_sol_fondos_aprob", "fecha_recibo_fondos_aprob",
    "comentarios", "estado",
    "asignacion_presup_final", "precio_acp",
)


def _autenticar(request):
    esperado = os.environ.get("DASHBOARD_EXPORT_TOKEN", "").strip()
    if not esperado:
        return HttpResponseForbidden("Endpoint no configurado (DASHBOARD_EXPORT_TOKEN vacío)")
    header = request.headers.get("Authorization", "")
    if not header.startswith("Token "):
        return HttpResponseForbidden("Falta header Authorization: Token <valor>")
    recibido = header[len("Token "):].strip()
    if not _secrets.compare_digest(recibido, esperado):
        return HttpResponseForbidden("Token inválido")
    return None


def _fmt_fecha(valor):
    if valor is None:
        return ""
    return valor.isoformat()


def _fmt_num(valor):
    if valor is None:
        return ""
    return str(valor)


@require_GET
def export_proyectos_cc_csv(request):
    denegado = _autenticar(request)
    if denegado:
        return denegado

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="Proyecto_CC.csv"'
    response.write("﻿")

    writer = csv.writer(response)
    writer.writerow(COLS_PROYECTOS)

    qs = Proyecto_CC.objects.all().order_by("codigo")
    for p in qs.iterator(chunk_size=500):
        writer.writerow([
            p.codigo or "",
            p.title or "",
            p.seccion or "",
            p.coordinador or "",
            _fmt_fecha(p.fecha_entrada),
            _fmt_fecha(p.fecha_envio_FIO),
            _fmt_fecha(p.fecha_sol_fondos_aprob),
            _fmt_fecha(p.fecha_recibo_fondos_aprob),
            (p.comentarios or "").replace("\r\n", " ").replace("\n", " "),
            _fmt_num(p.estado),
            _fmt_num(p.asignacion_presup_final),
            _fmt_num(p.precio_acp),
        ])
    return response


@require_GET
def export_proyecto_cc_licitacion_csv(request):
    denegado = _autenticar(request)
    if denegado:
        return denegado

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="Proyecto_CC_Licitacion.csv"'
    response.write("﻿")

    writer = csv.writer(response)
    writer.writerow(["CodigoProyecto", "RFQ"])

    qs = (Proyecto_CC_Licitacion.objects
          .select_related("proyecto_cc", "licitacion")
          .order_by("proyecto_cc__codigo"))
    for pl in qs.iterator(chunk_size=500):
        if pl.proyecto_cc_id is None or pl.licitacion_id is None:
            continue
        codigo = getattr(pl.proyecto_cc, "codigo", None)
        rfq = getattr(pl.licitacion, "rfq", None)
        if not codigo or not rfq:
            continue
        writer.writerow([codigo, rfq])
    return response
