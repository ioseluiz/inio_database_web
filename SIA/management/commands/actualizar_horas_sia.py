from django.core.management.base import BaseCommand
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from SIA.models import tblProyectos
import time

class Command(BaseCommand):
    """
    Este comando de django calcula la suma de horas (regulares, extras, compensatorias)
    para cada proyecto desde la tabla de transacciones y actualiza el campo 'HorasTotales'
    en el modelo tblProyectos

    Para ejecutar este comando:
    python manage.py actualizar_horas
    """

    help = 'Calcula y actualiza las horas totales cargadas para cada proyecto.'

    def handle(self, *args, **options):
        """
        El metodo principal que se ejecuta cuando se llama al comando.
        """
        self.stdout.write(self.style.SUCCESS("Iniciando el proceso de actualización de horas totales por proyecto..."))
        start_time = time.time()

        # Obtenemos todos los proyectos para iterar sobre ellos.
        proyectos = tblProyectos.objects.all()
        proyectos_count = proyectos.count()
        updated_count = 0
        skipped_count = 0

        if proyectos_count == 0:
            self.stdout.write(self.style.WARNING("No se encontraron proyectos en la base de datos."))
            return

        self.stdout.write(f"Se encontraron {proyectos_count} proyectos para procesar.")

        for i, proyecto in enumerate(proyectos):
            # Obtenemos el queryset de transacciones para este proyecto
            transacciones_qs = proyecto.transacciones.all()
            
            # Primero, verificamos si existen transacciones para evitar un cálculo innecesario
            if not transacciones_qs.exists():
                self.stdout.write(self.style.WARNING(
                    f"({i + 1}/{proyectos_count}) Proyecto '{proyecto.CodProyecto}' no tiene transacciones. HorasTotales se establece en 0."
                ))
                # Si el valor actual no es 0, lo actualizamos.
                if proyecto.HorasTotales != 0.0:
                    proyecto.HorasTotales = 0.0
                    proyecto.save(update_fields=['HorasTotales'])
                skipped_count += 1
                continue # Pasamos al siguiente proyecto

            # Si hay transacciones, realizamos la agregación
            resultado_suma = transacciones_qs.aggregate(
                total_calculado=Sum(
                    Coalesce(F('HoraRegular'), Value(0.0)) +
                    Coalesce(F('HoraExtra'), Value(0.0)) +
                    Coalesce(F('HoraComp'), Value(0.0))
                )
            )
            
            horas_totales_calculadas = resultado_suma.get('total_calculado') or 0.0

             # Actualizamos el campo y guardamos solo si el valor ha cambiado
            if proyecto.HorasTotales != horas_totales_calculadas:
                proyecto.HorasTotales = horas_totales_calculadas
                proyecto.save(update_fields=['HorasTotales'])
                updated_count += 1
                self.stdout.write(
                    f"({i + 1}/{proyectos_count}) Proyecto '{proyecto.CodProyecto}' ACTUALIZADO con {horas_totales_calculadas:.2f} horas."
                )
            else:
                 self.stdout.write(
                    f"({i + 1}/{proyectos_count}) Proyecto '{proyecto.CodProyecto}' ya está al día con {horas_totales_calculadas:.2f} horas."
                )


        end_time = time.time()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS("\n-- Resumen de la Actualización --"))
        self.stdout.write(f"Proyectos actualizados exitosamente: {updated_count}")
        self.stdout.write(f"Duración total del proceso: {duration:.2f} segundos.")
        self.stdout.write(self.style.SUCCESS("¡Proceso completado!"))
