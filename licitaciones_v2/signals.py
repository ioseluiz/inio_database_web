from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Propuesta, PropuestaDetalle


def _recalcular_totalmonto(propuesta_id):
    """
    Recalcula Propuesta.totalmonto como la suma de bid_line_amount
    de todos sus detalles. Usa .update() para evitar disparar signals
    en Propuesta y no tocar fecha_ultima_actualizacion (auto_now).
    Si la propuesta ya no existe (cascade delete), no hace nada.
    """
    total = PropuestaDetalle.objects.filter(bid_id=propuesta_id).aggregate(
        total=Sum('bid_line_amount')
    )['total'] or 0.0
    Propuesta.objects.filter(pk=propuesta_id).update(totalmonto=total)


@receiver(post_save, sender=PropuestaDetalle)
def propuesta_detalle_post_save(sender, instance, **kwargs):
    _recalcular_totalmonto(instance.bid_id)


@receiver(post_delete, sender=PropuestaDetalle)
def propuesta_detalle_post_delete(sender, instance, **kwargs):
    _recalcular_totalmonto(instance.bid_id)
