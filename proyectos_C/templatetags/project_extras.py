from django import template
from datetime import date, datetime, timedelta

register = template.Library()

@register.filter(name='days_between')
def days_between(date1, date2):
    """
    Calcula la diferencia en días entre dos fechas, manejando instancias
    de date y datetime de forma segura.
    """
    # Primero, se asegura de que ninguna de las fechas sea Nula
    if date1 is None or date2 is None:
        return "" # Devuelve una cadena vacía para no mostrar nada en el template

    # --- INICIO DE LA CORRECCIÓN ---
    # Si alguna de las variables es un objeto datetime, la convierte a solo fecha
    if isinstance(date1, datetime):
        date1 = date1.date()
    if isinstance(date2, datetime):
        date2 = date2.date()
    # --- FIN DE LA CORRECCIÓN ---

    # Ahora que ambos son objetos 'date', la resta es segura.
    # Usamos abs() para obtener siempre un número positivo, lo que simplifica el código.
    return abs((date1 - date2).days)


@register.filter(name='subtract_15_days')
def subtract_15_days(target_date):
    """
    Resta 15 días a la fecha proporcionada.
    Maneja instancias de date y datetime.
    """
    # Si la fecha es Nula, devuelve una cadena vacía
    if target_date is None:
        return ""

    # Si es un objeto datetime, se convierte a solo fecha
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    # Se realiza la resta de los 15 días usando timedelta
    return target_date - timedelta(days=15)

# --- FIN DEL NUEVO TEMPLATE TAG ---