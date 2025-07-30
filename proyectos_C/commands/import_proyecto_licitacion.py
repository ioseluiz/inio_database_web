import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from proyectos_C.models import Proyecto_CC, Proyecto_CC_Licitacion
from licitaciones.models import Licitacion

class Command(BaseCommand):
    help = 'Importa datos de Proyectos_CC_Licitacion desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Ruta al archivo CSV con los datos a importar'
        )

        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecuta una simulacion sin guardar datos en la base de datos'
        )

        parser.add_argument(
            '--skip-duplicates',
            action='store_true',
            help='Omite registros duplicados en lugar de fallar'
        )


    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        dry_run = options['dry_run']
        skip_duplicates = options['skip_duplicates']


        # Verificar que existe el archivo
        if not os.path.exists(csv_file_path):
            raise CommandError(f'El archivo {csv_file_path} no existe.')
        
        # Contadores para el reporte
        success_count = 0
        error_count = 0
        duplicate_count = 0
        errors = []

        self.stdout.write(f'Iniciando importacion desde: {csv_file_path}')
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: No SE guardaran datos'))

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                # Detectar el delimitador automaticamente
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimeter = sniffer.sniff(sample).delimiter

                reader = csv.DictReader(file, delimiter=delimeter)

                # Verificar que las columnas necesarias esten presentes
                required_columns = ['proyecto_cc', 'licitacion']
                missing_columns = [col for col in required_columns if col not in reader.fieldnames]

                if missing_columns:
                    raise CommandError(
                        f'Faltan las siguientes columnas en el CSV: {", ".join(missing_columns)}\n'
                        f'Columnas disponibles: {", ".join(reader.fieldnames)}'
                    )
                
                # Procesar cada fila
                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            # Limpiar datos
                            proyecto_cc = row['proyecto_cc'].strip()
                            licitacion = row['licitacion'].strip()

                            # Validar que no esten vacios
                            if not proyecto_cc or not licitacion:
                                error_msg = f'Fila {row_num}: Codigo de proyecto o RFQ de licitacion'
                                errors.append(error_msg)
                                error_count += 1
                                continue

                            # Buscar el proyecto_CC
                            try:
                                proyecto_cc = Proyecto_CC.objects.get(codigo=proyecto_cc)
                            except Proyecto_CC.DoesNotExist:
                                error_msg = f'Fila {row_num}: No existe Proyecto_CC con codigo "{proyecto_cc}"'
                                errors.append(error_msg)
                                error_count += 1
                                continue

                            # Buscar la licitacion
                            try:
                                rfq_licitacion = Licitacion.objects.get(rfq=licitacion)
                            except Licitacion.DoesNotExist:
                                error_msg = f'Fila {row_num}: No existe Proyecto_CC con codigo "{proyecto_cc}"'
                                errors.append(error_msg)
                                error_count += 1
                                continue

                            # Usar get_or_create para manejar duplicados automaticamente
                            if not dry_run:
                                relacion, created = Proyecto_CC_Licitacion.objects.get_or_create(
                                    proyecto_cc=proyecto_cc,
                                    licitacion=licitacion
                                )

                                if created:
                                    # Es un registro nuevo
                                    pass
                                else:
                                    # Ya existia una relacion
                                    if skip_duplicates:
                                        duplicate_count += 1
                                        self.stdout.write(
                                            self.style.WARNING(
                                                f'Fila {row_num}: Relacion ya existia -'
                                                f'Proyecto: {proyecto_cc}, Licitacion: {rfq_licitacion}'
                                            )
                                        )
                                        continue

                            else:
                                # En modo dry-run, verificar manualmente
                                if Proyecto_CC_Licitacion.objects.filter(
                                    proyecto_cc=proyecto_cc,
                                    licitacion=rfq_licitacion
                                ).exists():
                                    if skip_duplicates:
                                        duplicate_count += 1
                                        self.stdout.write(
                                            self.stye.WARNING(
                                                f'Fila {row_num}: Relacion duplicada (dry-run) -'
                                                f'Proyecto: {proyecto_cc}, Licitacion: {licitacion}'
                                            )
                                        )
                                        continue
                                    else:
                                        error_msg = (
                                            f'Fila {row_num}: Ya existe la relación entre '
                                            f'Proyecto "{proyecto_cc}" y Licitación "{licitacion}"'

                                        )
                                        errors.append(error_msg)
                                        error_count += 1
                                        continue

                            success_count += 1
                            self.stdout.write(
                                f'Fila {row_num}: ✓ Proyecto: {proyecto_cc} → Licitación: {licitacion}'
                            )

                        except Exception as e:
                            error_msg = f'Fila {row_num}: Error inesperado - {str(e)}'
                            errors.append(error_msg)
                            error_count += 1

                    if dry_run:
                        transaction.set_rollback(True)

        except Exception as e:
            raise CommandError(f'Error al procesar el archivo: {str(e)}')
        
        # Mostrar reporte final
        self.stdout.write('\n' + '='*50)
        self.stdout.write('REPORTE DE IMPORTACION')
        self.stdout.write('='*50)

        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN - Sin cambios en la base de datos'))

        self.stdout.write(f'Registros procesados exitosamente: {success_count}')
        if duplicate_count > 0:
            self.stdout.write(f'Registros duplicados omitidos: {duplicate_count}')
        self.stdout.write(f'Registros con errores: {error_count}')

        # Mostrar errores si los hay
        if errors:
            self.stdout.write('\nERRORES ENCONTRADOS:')
            for error in errors[:10]:  # Mostrar solo los primeros 10 errores
                self.stdout.write(self.style.ERROR(f'  • {error}'))
            
            if len(errors) > 10:
                self.stdout.write(f'  ... y {len(errors) - 10} errores más')

        # Mensaje final
        if error_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Importación completada exitosamente. '
                    f'Se procesaron {success_count} registros.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠ Importación completada con {error_count} errores. '
                    f'Se procesaron {success_count} registros exitosamente.'
                )
            )


                

