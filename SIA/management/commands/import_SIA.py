import os
import pyodbc
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError
from dotenv import load_dotenv
from django.utils import timezone
from SIA.models import tblProyectos

# Cargar variables de entorno desde archivo .env en la raiz del proyecto
load_dotenv()

class Command(BaseCommand):
    """
    Este comando Django se conecta a una base de datos SQL Server remota,
    lee los datos de la tabla 'tblProyectos' y los sincroniza con el modelo local SIA.

    Para ejecutar este comando:
    python manage.py import_SIA
    """

    help = 'Conecta a una base de datos SQL Server remota y actualiza el modelo SIA de Django.'

    def handle(self, *args, **options):
        """
        El metodo principal que se ejecuta cuando se llama al comando.
        Aqui se encuentra toda la logica de conexion y sincronizacion
        """
        self.stdout.write(self.style.SUCCESS("Iniciando el proceso de actualizacion del modelo SIA..."))

        # -- Obtener parametros de conexion desde variables de entorno --
        db_driver = os.getenv('DB_DRIVER_SQLSERVER')
        self.stdout.write(f"{db_driver}")
        db_server = os.getenv('DB_SERVER_SQLSERVER')
        db_name = os.getenv('DB_NAME_SQLSERVER')
        db_username = os.getenv('DB_USERNAME_SQLSERVER')
        db_password = os.getenv('DB_PASSWORD_SQLSERVER')

        # Verificacion de que todas las variables de entorno necesarias esten presentes
        if not all([db_driver, db_server, db_name, db_username, db_password]):
            raise CommandError(
                "Una o mas variables de entorno de la base de datos no estan configuradas. "
                "Asegurate de que DB_DRIVER, DB_SERVER, DB_NAME, DB_USERNAME y DB_PASSWORD"
                "esten en tu archivo .env"
            )
        
        # Cadena de conexion para pyodbc
        conn_str = f"DRIVER={db_driver};SERVER={db_server};DATABASE={db_name};UID={db_username};PWD={db_password}"

        remote_conn = None
        try:

            # -- Conexion a la base de datos remota --
            self.stdout.write(f"Conectando a la base de datos '{db_name}' en el servidor '{db_server}...'")
            remote_conn = pyodbc.connect(conn_str)
            cursor = remote_conn.cursor()
            self.stdout.write(self.style.SUCCESS("Conexion exitosa a la base de datos SQL SERVER remota."))

            # -- Consulta a la tabla remota --
            # Seleccionamos las columnas que coinciden con el modelo tblProyectos
            query = """
                    SELECT
                    CodProyecto, NomProyecto, CodCuenta, CodRamo, CodCliente,
                    Prioridad, TipoCosto, Fiscal, DescProyecto, FechaRec,
                    FechaIni, FechaEIES, FechaEst, FechaReal, IPCoordinador, Abierto
                    FROM tblProyectos
                    """
            self.stdout.write("Ejecutando consulta en la tabla remote 'tblProyectos'...")
            cursor.execute(query)

            remote_rows = cursor.fetchall()
            self.stdout.write(f"Se encontraron {len(remote_rows)} registros en la tabla remota.")

            # -- Sincronizacion de datos --
            created_count = 0
            updated_count = 0
            failed_count = 0

            for i, row in enumerate(remote_rows):
                try:
                    # Mapeo de datos de la fila a un  diccionario para facilitar el manejo
                    data = {
                        'NomProyecto': row.NomProyecto,
                        # Si el valor es una cadena vacía o None, se guarda como None.
                        'CodCuenta': int(row.CodCuenta) if row.CodCuenta not in [None, ''] else None,
                        'CodRamo': row.CodRamo,
                        'CodCliente': row.CodCliente,
                        'Prioridad': int(row.Prioridad) if row.Prioridad not in [None, ''] else None,
                        'TipoCosto': row.TipoCosto,
                        'Fiscal': int(row.Fiscal) if row.Fiscal not in [None, ''] else None,
                        'DescProyecto': row.DescProyecto,
                        # La función _make_aware_date ahora maneja la zona horaria
                        'FechaRec': self._make_aware_date(row.FechaRec),
                        'FechaIni': self._make_aware_date(row.FechaIni),
                        'FechaEIES': self._make_aware_date(row.FechaEIES),
                        'FechaEst': self._make_aware_date(row.FechaEst),
                        'FechaReal': self._make_aware_date(row.FechaReal),
                        'IPCoordinador': row.IPCoordinador,
                        'Abierto': int(row.Abierto) if row.Abierto not in [None, ''] else None
                    }

                    # Usamos update_or_create para simplificar la logica.
                    # Busca un objeto con el CodProyecto dado. Si la encuentra, lo actualiza.
                    # Si no lo encuentra, crea uno nuevo.
                    obj, created = tblProyectos.objects.update_or_create(
                        CodProyecto=row.CodProyecto,
                        defaults=data
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(f"CREADO nuevo SIA: {row.CodProyecto}")
                    else:
                        # update_or_create ya maneja la actualizacion.
                        # Podemos agregar un log para saber que fue verificado
                        updated_count += 1 # contamos como verificado/actualizado
                        self.stdout.write(f"VERIFICADO/ACTUALIZADO SIA: {row.CodProyecto}")

                except (ValueError, TypeError, IntegrityError) as e:
                    # Captura errores si la conversión de datos falla para una fila específica
                    self.stderr.write(self.style.ERROR(
                        f"\nError al procesar la fila {i+1} (CodProyecto: {row.CodProyecto}): {e}"
                    ))
                    self.stderr.write(f"  -> Datos de la fila problemática: {dict(zip([c[0] for c in cursor.description], row))}")
                    failed_count += 1

            self.stdout.write(self.style.SUCCESS("\n-- Resumen de la Sincronizacion --"))
            self.stdout.write(f"SIA nuevos creados: {created_count}")
            self.stdout.write(f"SIA existentes verificados/actualizados: {updated_count - created_count}")
            self.stdout.write(f"Total de registros procesados: {len(remote_rows)}")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            self.stderr.write(self.style.ERROR(f"Error de base de datos al conectar o ejecutar la consulta: {sqlstate}"))
            self.stderr.write(self.style.ERROR(ex))
            raise CommandError("No se pudo completar la operación debido a un error de base de datos.")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ha ocurrido un error inesperado: {e}"))
            raise CommandError("La operación falló inesperadamente.")
        finally:
            # Aseguramos que la conexión se cierre siempre
            if remote_conn:
                remote_conn.close()
                self.stdout.write(self.style.SUCCESS("Conexión a la base de datos remota cerrada."))

    def _make_aware_date(self, date_value):
        """
        Convierte un valor de fecha a un objeto datetime "aware" (consciente de la zona horaria).
        """
        if date_value is None:
            return None

        # Parsea si es un string
        if isinstance(date_value, str):
            dt_object = parse_datetime(date_value)
        else:
            dt_object = date_value
        
        if dt_object is None:
            return None

        # Si la fecha es "naive", la hace "aware" usando la zona horaria del proyecto
        if timezone.is_naive(dt_object):
            return timezone.make_aware(dt_object)
        
        return dt_object


