import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Asegúrate de importar los modelos correctos de sus respectivas aplicaciones
from proyectos_C.models import Proyecto_CC, Proyecto_CC_Licitacion
from licitaciones.models import Licitacion # Asumiendo que Licitacion está en una app 'licitaciones'


class Command(BaseCommand):
    """
    Comando de Django para importar y vincular Proyectos CC con Licitaciones desde un archivo CSV.

    El CSV debe tener las columnas 'No. Estimado' (código del Proyecto_CC) y 
    'licitacion' (RFQ de la Licitacion).

    Uso:
        python manage.py importar_proyectos_licitaciones /ruta/al/archivo/proyectos_cc_licitaciones.csv
    """
    help = 'Importa y vincula datos de licitaciones a proyectos CC desde un archivo CSV.'

    def add_arguments(self, parser):
        """
        Agrega el argumento posicional para la ruta del archivo CSV.
        """
        parser.add_argument('csv_file_path', type=str, help='La ruta completa al archivo CSV a importar.')

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Lógica principal del comando.
        """
        csv_file_path = options['csv_file_path']

        # 1. Verificar que el archivo existe
        if not os.path.exists(csv_file_path):
            raise CommandError(f"El archivo '{csv_file_path}' no fue encontrado.")

        self.stdout.write(self.style.SUCCESS(f"Iniciando la importación desde '{csv_file_path}'..."))

        # Contadores para el resumen final
        creados = 0
        actualizados = 0
        omitidos = 0
        
        # 2. Abrir y leer el archivo CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            # Usamos DictReader para acceder a las columnas por su nombre
            reader = csv.DictReader(csvfile)
            
            for index, row in enumerate(reader, start=2): # start=2 para contar la línea del header
                proyecto_cc_codigo = row.get('No. Estimado', '').strip()
                licitacion_rfq = row.get('licitacion', '').strip()

                # Omitir filas vacías o con datos incompletos
                if not proyecto_cc_codigo or not licitacion_rfq:
                    self.stdout.write(self.style.WARNING(f"Línea {index}: Omitida. Faltan datos ('{proyecto_cc_codigo}', '{licitacion_rfq}')."))
                    omitidos += 1
                    continue

                try:
                    # 3. Verificar que tanto el proyecto como la licitación existan
                    proyecto = Proyecto_CC.objects.get(codigo=proyecto_cc_codigo)
                    licitacion = Licitacion.objects.get(rfq=licitacion_rfq)
                    
                    # 4. Crear o actualizar el registro de vinculación
                    # update_or_create busca un registro con los parámetros proporcionados.
                    # Si lo encuentra, lo actualiza con los 'defaults'. Si no, crea uno nuevo.
                    # En este caso, no hay campos que actualizar, solo asegurar la existencia.
                    obj, created = Proyecto_CC_Licitacion.objects.update_or_create(
                        proyecto_cc=proyecto,
                        licitacion=licitacion,
                        defaults={} # No hay campos adicionales para actualizar
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Línea {index}: Creado enlace para Proyecto {proyecto.codigo} y Licitación {licitacion.rfq}."))
                        creados += 1
                    else:
                        self.stdout.write(f"Línea {index}: El enlace para {proyecto.codigo} y {licitacion.rfq} ya existía.")
                        actualizados += 1

                except Proyecto_CC.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Línea {index}: Omitida. El Proyecto_CC con código '{proyecto_cc_codigo}' no existe."))
                    omitidos += 1
                    continue # Pasar a la siguiente fila
                except Licitacion.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Línea {index}: Omitida. La Licitacion con RFQ '{licitacion_rfq}' no existe."))
                    omitidos += 1
                    continue # Pasar a la siguiente fila
                except Exception as e:
                    raise CommandError(f"Error en la línea {index}: {e}")

        # Mensaje final con resumen
        self.stdout.write(self.style.SUCCESS("\nProceso de importación finalizado."))
        self.stdout.write(f"Resumen: {creados} registros creados, {actualizados} ya existían, {omitidos} filas omitidas.")