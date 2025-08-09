from django.core.management.base import BaseCommand
from django.db.models import Sum, F, Value, Q
from django.db.models.functions import Coalesce
from SIA.models import tblProyectos # Asegúrate que la ruta de importación sea la correcta
import time

class Command(BaseCommand):
    """
    Este comando de django calcula la suma de horas (regulares, extras, compensatorias)
    para cada proyecto desde la tabla de transacciones y actualiza los campos 'HorasTotales',
    'horas_estimador' y 'horas_especificador' en el modelo tblProyectos.

    Para ejecutar este comando:
    python manage.py actualizar_horas_sia
    """

    help = 'Calcula y actualiza las horas totales, de estimador y de especificador para cada proyecto.'

    def handle(self, *args, **options):
        """
        El metodo principal que se ejecuta cuando se llama al comando.
        """
        self.stdout.write(self.style.SUCCESS("Iniciando el proceso de actualización de horas por proyecto..."))
        start_time = time.time()

        proyectos = tblProyectos.objects.all()
        proyectos_count = proyectos.count()
        updated_count = 0
        
        if proyectos_count == 0:
            self.stdout.write(self.style.WARNING("No se encontraron proyectos en la base de datos."))
            return

        self.stdout.write(f"Se encontraron {proyectos_count} proyectos para procesar.")

        for i, proyecto in enumerate(proyectos):
            transacciones_qs = proyecto.transacciones.all()
            
            # Expresión base para la suma de horas
            suma_horas_expr = Coalesce(F('HoraRegular'), Value(0.0)) + \
                              Coalesce(F('HoraExtra'), Value(0.0)) + \
                              Coalesce(F('HoraComp'), Value(0.0))

            # 1. Calcular Horas Totales (sin filtro de CodRamo)
            resultado_total = transacciones_qs.aggregate(total_calculado=Sum(suma_horas_expr))
            horas_totales_calculadas = resultado_total.get('total_calculado') or 0.0

            # 2. Calcular Horas Estimador (CodRamo = 'INIOES')
            resultado_estimador = transacciones_qs.filter(CodRamo="INIOES").aggregate(
                total_calculado=Sum(suma_horas_expr)
            )
            horas_estimador_calculadas = resultado_estimador.get('total_calculado') or 0.0

            # 3. Calcular Horas Especificador (CodRamo = 'INIOCE')
            resultado_especificador = transacciones_qs.filter(CodRamo="INIOCE").aggregate(
                total_calculado=Sum(suma_horas_expr)
            )
            horas_especificador_calculadas = resultado_especificador.get('total_calculado') or 0.0

            # Lista de campos a actualizar
            update_fields = []
            
            # Comprobar y añadir campos si han cambiado
            if proyecto.HorasTotales != horas_totales_calculadas:
                proyecto.HorasTotales = horas_totales_calculadas
                update_fields.append('HorasTotales')

            if proyecto.horas_estimador != horas_estimador_calculadas:
                proyecto.horas_estimador = horas_estimador_calculadas
                update_fields.append('horas_estimador')

            if proyecto.horas_especificador != horas_especificador_calculadas:
                proyecto.horas_especificador = horas_especificador_calculadas
                update_fields.append('horas_especificador')

            # Guardar solo si hay cambios
            if update_fields:
                proyecto.save(update_fields=update_fields)
                updated_count += 1
                self.stdout.write(
                    f"({i + 1}/{proyectos_count}) Proyecto '{proyecto.CodProyecto}' ACTUALIZADO. "
                    f"Totales: {horas_totales_calculadas:.2f}, "
                    f"Estimador: {horas_estimador_calculadas:.2f}, "
                    f"Especificador: {horas_especificador_calculadas:.2f}"
                )
            else:
                 self.stdout.write(
                    f"({i + 1}/{proyectos_count}) Proyecto '{proyecto.CodProyecto}' ya está al día."
                )

        end_time = time.time()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS("\n-- Resumen de la Actualización --"))
        self.stdout.write(f"Proyectos procesados: {proyectos_count}")
        self.stdout.write(f"Proyectos actualizados: {updated_count}")
        self.stdout.write(f"Duración total del proceso: {duration:.2f} segundos.")
        self.stdout.write(self.style.SUCCESS("¡Proceso completado!"))
