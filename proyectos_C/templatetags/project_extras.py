from django import template
from datetime import date, datetime

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