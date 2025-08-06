import os
import pyodbc
import datetime # Importado para timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError, transaction
from dotenv import load_dotenv
from django.utils import timezone
from SIA.models import tblProyectos, tblTransacciones

# Cargar variables de entorno desde archivo .env en la raiz del proyecto.
load_dotenv()

class Command(BaseCommand):
    """
    Este comando Django se conecta a una base de datos SQL Server remota,
    lee los datos de la tabla 'tblTransacciones' y las sincroniza con el modelo local.

    Para ejecutar este comando:
    python manage.py import_transacciones
    python manage.py import_transacciones --days 30
    """

    help = 'Conecta a una base de datos SQL Server remota y actualiza el modelo tblTransacciones de Django.'

    def add_arguments(self, parser):
        """Añade argumentos opcionales al comando"""
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Número de registros a procesar por lote (default: 1000)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecuta el comando sin hacer cambios en la base de datos'
        )
        # ---> INICIO DE MODIFICACIÓN <---
        parser.add_argument(
            '--days',
            type=int,
            default=None, # Por defecto es None para procesar todo si no se especifica
            help='Sincroniza solo los últimos X días. Si no se especifica, sincroniza todo el historial.'
        )
        # ---> FIN DE MODIFICACIÓN <---

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        # ---> INICIO DE MODIFICACIÓN <---
        days = options['days']
        # ---> FIN DE MODIFICACIÓN <---
        verbosity = options.get('verbosity', 1)

        if dry_run:
            self.stdout.write(self.style.WARNING("MODO DRY-RUN: No se realizarán cambios en la base de datos."))

        # Validación de variables de entorno
        required_env_vars = ['DB_DRIVER_SQLSERVER', 'DB_SERVER_SQLSERVER', 'DB_NAME_SQLSERVER', 'DB_PASSWORD_SQLSERVER']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]

        if missing_vars:
            raise CommandError(f"Las siguientes variables de entorno no están configuradas: {', '.join(missing_vars)}")

        db_driver = os.getenv('DB_DRIVER_SQLSERVER')
        db_server = os.getenv('DB_SERVER_SQLSERVER')
        db_name = os.getenv('DB_NAME_SQLSERVER')
        db_username = os.getenv('DB_USERNAME_SQLSERVER')
        db_password = os.getenv('DB_PASSWORD_SQLSERVER')

        conn_str = f"DRIVER={db_driver};SERVER={db_server};DATABASE={db_name};UID={db_username};PWD={db_password}"

        remote_conn = None
        try:
            self.stdout.write(f"Conectando a la base de datos '{db_name}' en el servidor '{db_server}'...")
            remote_conn = pyodbc.connect(conn_str)
            cursor = remote_conn.cursor()
            self.stdout.write(self.style.SUCCESS("Conexión exitosa a la base de datos SQL Server remota."))

            # ---> INICIO DE MODIFICACIÓN <---
            # Construcción dinámica de la query
            query = """
                SELECT Fecha, IP, CodProyecto, HoraRegular, HoraExtra, HoraComp, CodRamo
                FROM tblTransacciones
            """
            params = []

            if days is not None:
                if days < 0:
                    raise CommandError("El número de días no puede ser negativo.")
                self.stdout.write(self.style.NOTICE(f"Sincronizando transacciones de los últimos {days} días."))
                # Calcular la fecha de inicio para el filtro
                start_date = timezone.now() - datetime.timedelta(days=days)
                # Añadir la condición WHERE a la query
                query += " WHERE Fecha >= ?"
                # Añadir el valor del parámetro de forma segura
                params.append(start_date.strftime('%Y-%m-%d %H:%M:%S'))

            query += " ORDER BY CodProyecto DESC"

            self.stdout.write("Ejecutando consulta en la tabla remota 'tblTransacciones'...")
            # Ejecutar la query con los parámetros
            cursor.execute(query, params)
            # ---> FIN DE MODIFICACIÓN <---

            # El resto del código permanece igual...
            created_count = 0
            updated_count = 0
            failed_count = 0
            skipped_count = 0
            total_processed = 0

            proyectos_cache = {}

            while True:
                remote_rows = cursor.fetchmany(batch_size)
                if not remote_rows:
                    break

                self.stdout.write(f"Procesando lote de {len(remote_rows)} registros...")
                
                with transaction.atomic():
                    batch_created, batch_updated, batch_failed, batch_skipped = self._process_batch(
                        remote_rows, proyectos_cache, dry_run, verbosity
                    )
                    
                    created_count += batch_created
                    updated_count += batch_updated
                    failed_count += batch_failed
                    skipped_count += batch_skipped
                    total_processed += len(remote_rows)

                self.stdout.write(f"Lote procesado. Total acumulado: {total_processed} registros")

            self._print_summary(created_count, updated_count, skipped_count, failed_count, total_processed, dry_run)

        except pyodbc.Error as ex:
            sqlstate = ex.args[0] if ex.args else "Unknown"
            self.stderr.write(self.style.ERROR(f"Error de base de datos SQL Server: {sqlstate}"))
            self.stderr.write(self.style.ERROR(str(ex)))
            raise CommandError("No se pudo completar la operación debido a un error de base de datos.")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ha ocurrido un error inesperado: {e}"))
            raise CommandError("La operación falló inesperadamente.")
        finally:
            if remote_conn:
                remote_conn.close()
                self.stdout.write(self.style.SUCCESS("Conexión a la base de datos remota cerrada."))

    def _process_batch(self, remote_rows, proyectos_cache, dry_run, verbosity):
        """Procesa un lote de registros"""
        created_count = 0
        updated_count = 0
        failed_count = 0
        skipped_count = 0

        for i, row in enumerate(remote_rows):
            try:
                cod_proyecto = row.CodProyecto
                if cod_proyecto not in proyectos_cache:
                    try:
                        proyectos_cache[cod_proyecto] = tblProyectos.objects.get(CodProyecto=cod_proyecto)
                    except tblProyectos.DoesNotExist:
                        proyectos_cache[cod_proyecto] = None

                proyecto_obj = proyectos_cache[cod_proyecto]
                if proyecto_obj is None:
                    self.stderr.write(self.style.WARNING(
                        f"Saltando registro: El proyecto '{cod_proyecto}' no existe en la base de datos local."
                    ))
                    skipped_count += 1
                    continue

                fecha_aware = self._make_aware_date(row.Fecha)
                if fecha_aware is None:
                    self.stderr.write(self.style.WARNING(
                        f"Saltando registro: Fecha inválida para proyecto '{cod_proyecto}'"
                    ))
                    skipped_count += 1
                    continue

                hora_regular = self._validate_hours(row.HoraRegular, 'HoraRegular')
                hora_extra = self._validate_hours(row.HoraExtra, 'HoraExtra')
                hora_comp = self._validate_hours(row.HoraComp, 'HoraComp')

                defaults_data = {
                    'HoraRegular': hora_regular,
                    'HoraExtra': hora_extra,
                    'HoraComp': hora_comp,
                    'CodRamo': row.CodRamo,
                }

                if not dry_run:
                    obj, created = tblTransacciones.objects.update_or_create(
                        Fecha=fecha_aware,
                        IP=row.IP,
                        CodProyecto=proyecto_obj,
                        defaults=defaults_data
                    )

                    if created:
                        created_count += 1
                        if verbosity >= 2:
                            self.stdout.write(f"CREADA nueva transacción para proyecto: {cod_proyecto}")
                    else:
                        updated_count += 1
                        if verbosity >= 2:
                            self.stdout.write(f"ACTUALIZADA transacción para proyecto: {cod_proyecto}")
                else:
                    existing = tblTransacciones.objects.filter(
                        Fecha=fecha_aware,
                        IP=row.IP,
                        CodProyecto=proyecto_obj
                    ).exists()
                    
                    if existing:
                        updated_count += 1
                    else:
                        created_count += 1

            except (ValueError, TypeError, IntegrityError) as e:
                self.stderr.write(self.style.ERROR(
                    f"Error al procesar registro (Proyecto: {row.CodProyecto}, Fecha: {row.Fecha}): {e}"
                ))
                failed_count += 1

        return created_count, updated_count, failed_count, skipped_count

    def _validate_hours(self, hour_value, field_name):
        """Valida que las horas sean valores válidos y no negativos"""
        if hour_value is None:
            return None
        
        try:
            hours = float(hour_value)
            if hours < 0:
                self.stderr.write(self.style.WARNING(
                    f"Valor negativo encontrado en {field_name}: {hours}. Se establecerá como 0."
                ))
                return 0.0
            return hours
        except (ValueError, TypeError):
            self.stderr.write(self.style.WARNING(
                f"Valor inválido en {field_name}: {hour_value}. Se establecerá como None."
            ))
            return None

    def _make_aware_date(self, date_value):
        """Convierte una fecha a timezone-aware"""
        if date_value is None:
            return None
        
        try:
            if isinstance(date_value, str):
                dt_object = parse_datetime(date_value)
            else:
                dt_object = date_value
            
            if dt_object is None:
                return None
            
            if timezone.is_naive(dt_object):
                return timezone.make_aware(dt_object)
            return dt_object
        except Exception:
            return None

    def _print_summary(self, created_count, updated_count, skipped_count, failed_count, total_processed, dry_run):
        """Imprime el resumen de la operación"""
        mode_text = " (MODO DRY-RUN)" if dry_run else ""
        self.stdout.write(self.style.SUCCESS(f"\n-- Resumen de la Sincronización de Transacciones{mode_text} --"))
        self.stdout.write(f"Transacciones nuevas {'que se crearían' if dry_run else 'creadas'}: {created_count}")
        self.stdout.write(f"Transacciones existentes {'que se actualizarían' if dry_run else 'actualizadas'}: {updated_count}")
        self.stdout.write(f"Transacciones saltadas (proyecto no encontrado): {skipped_count}")
        self.stdout.write(f"Transacciones con error: {failed_count}")
        self.stdout.write(f"Total de registros procesados: {total_processed}")
        
        if failed_count > 0:
            self.stdout.write(self.style.WARNING(f"Se encontraron {failed_count} errores durante el procesamiento."))
        elif created_count > 0 or updated_count > 0:
            self.stdout.write(self.style.SUCCESS("Sincronización completada exitosamente."))