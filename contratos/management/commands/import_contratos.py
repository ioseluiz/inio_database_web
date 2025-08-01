import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from datetime import datetime

from contratos.models import Contrato

# Mapeo de columnas del Excel a los campos del modelo Django
# Ayuda a modificar nombre si hay cambios en el archivo a futuro
COLUMN_MAPPING = {
    'PO': 'numero_contrato',
    'PO Header Description': 'description',
    'PO B/S/O': 'rubro',
    'PO Procurement Method': 'tipo_licitacion',
    'PO RFQ': 'numero_licitacion',
    'PO BID': 'numero_propuesta_ganadora',
    'PO Closed Status': 'status',
    'PO Closed Date': 'fecha_cierre',
    'PO First Approve Date': 'fecha_adjudicacion',
    'PO Fiscal Year': 'fiscal_year',
    'PO Fiscal Month': 'fiscal_month',
    'PO Vendor Name': 'vendor_name',
    'PO Original Amount': 'monto_contrato_original',
    'PO Billed Amount': 'monto_pagado',
    'PO Max Promised Date': 'fecha_promesa',
    'PO Max Due Date': 'fecha_maxima_entrega',
}

class Command(BaseCommand):
    help = 'Carga o actualiza contratos desde un archivo XLSX. El numero de contrato (PO) se usa como identificador unico'

    def add_arguments(self, parser):
        """
        Agrega el argumento para la ruta del archivo al comando.
        """
        parser.add_argument('file_path', type=str, help='La ruta completa al archivo XLSX a procesr.')

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Logica principal del comanndo
        """
        file_path = options['file_path']
        self.stdout.write(self.style.SUCCESS(f"Iniciando el procesamiento del archivo: {file_path}"))

        try:
            # Lee el archivo excel. 'openpyxl' es necesario para archivos .xlsx
            df = pd.read_excel(file_path, engine='openpyxl')
        except FileNotFoundError:
            raise CommandError(f"Error: El archivo no fue encontrado en la ruta: {file_path}")
        except Exception as e:
            raise CommandError(f"Error al leer el archivo Excel. Asegurate de que 'openpyxl' este instalado (`pip install openpyxl`). Error: {e}")
        
        # Reemplaza los valores NaN (Not a number) de pandas con None de Python
        df = df.where(pd.notnull(df), None)

        # Contadores para el resumen final
        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_list = []

        # Itera sobre cada fila del Dataframe
        for index, row in df.iterrows():
            numero_contrato_val = row.get('PO')

            # Salta la fila si el numero de contrato (PO) esta vacio
            if not numero_contrato_val:
                error_list.append(f"Fila {index + 2}: Se omitio porque la columna 'PO' esta vacia.")
                continue

            try:
                # Busca si el contrato ya existe o crea una nueva instancia en memoria
                contrato, created = Contrato.objects.get_or_create(
                    numero_contrato=str(numero_contrato_val)
                )

                # Prepara un diccionario con los datos de la fila del Excel
                update_fields = {}
                has_changes = False

                for col_name, field_name in COLUMN_MAPPING.items():
                    if col_name != 'PO' and col_name in row:
                        new_value = row[col_name]

                        # -- Limpieza y conversion de datos ---
                        # Convierte a None si es un string vaio o 'N/A' para campos no textuales
                        if pd.isna(new_value) or str(new_value).strip() in ['', 'N/A', '%']:
                            new_value = None

                        # Convierte campos de fecha
                        if field_name in ['fecha_cierre', 'fecha_adjudicacion', 'fecha_promesa', 'fecha_maxima_entrega'] and new_value:
                            try:
                                # usar pd.to_datetime es flexible con los formatos
                                new_value = pd.to_datetime(new_value)
                            except (ValueError, TypeError):
                                error_list.append(f"Fila {index + 2} (Contrato {numero_contrato_val}): Formato de fecha invalido para '{col_name}'. Valor: '{row[col_name]}'.")
                                new_value = getattr(contrato, field_name) # Mantiene el valor anterior si hay error

                        # Convierte campos numericos
                        if field_name in ['fiscal_year', 'fiscal_month', 'monto_contrato_original', 'monto_pagado'] and new_value is not None:
                            try:
                                if field_name in ['fiscal_year', 'fiscal_month']:
                                    new_value = int(float(new_value))
                                else:
                                    new_value = float(new_value)
                            except (ValueError, TypeError):
                                error_list.append(f"Fila {index + 2} (Contrato {numero_contrato_val}): Valor numérico inválido para '{col_name}'. Valor: '{row[col_name]}'.")
                                new_value = getattr(contrato, field_name)

                        # Compara el valor nuevo con el existente en el modelo
                        current_value = getattr(contrato, field_name)

                        # Manejo especial para la comparacion de fechas (timezone)
                        if isinstance(current_value, datetime) and isinstance(new_value, datetime):
                            # Ignora la informacion de zona horaria si uno la tiene y el otro no
                            if current_value.tzinfo and not new_value.tzinfo:
                                current_value = current_value.replace(tzinfo=None)
                            elif not current_value.tzinfo and new_value.tzinfo:
                                new_value = new_value.replace(tzinfo=None)

                        if str(current_value or '') != str(new_value or ''):
                            has_changes = True

                        update_fields[field_name] = new_value

                # Si es nuevo registro, se guarda directamente
                if created:
                    for field, value in update_fields.items():
                        setattr(contrato, field, value)
                    contrato.save()
                    created_count += 1

                # Si el registro ya existe y tiene cambios, se actualiza
                elif has_changes:
                    for field, value in update_fields.items():
                        setattr(contrato, field, value)
                    contrato.save()
                    updated_count += 1

                # Si no hay cambios, se omite
                else:
                    skipped_count += 1

            except Exception as e:
                # Captura cualquier otro error durante el procesamiento de la fila
                error_list.append(f"Fila {index + 1} (Contrato {numero_contrato_val}): Error inesperado - {e}")

        # -- Impresion del Resumen final
        self.stdout.write(self.style.SUCCESS("\n" + "="*50))
        self.stdout.write(self.style.SUCCESS(" Resument de la Carga de Contratos ".center(50, "=")))
        self.stdout.write(self.style.SUCCESS("="*50))
        self.stdout.write(f"Nuevos registros creados: {created_count}")
        self.stdout.write(f"Registros existentes actualizados: {updated_count}")
        self.stdout.write(f"Registros sin cambios (omitidos): {skipped_count}")
        self.stdout.write(self.style.WARNING(f"Registros con errores: {len(error_list)}"))
        self.stdout.write(self.style.SUCCESS("="*50 + "\n"))

        if error_list:
            self.stdout.write(self.style.ERROR("Detalle de errores encontrados: "))
            for error in error_list:
                self.stdout.write(self.style.ERROR(f"- {error}"))
            self.stdout.write("\n")
        self.stdout.write(self.style.SUCCESS("Proceso de carga finalizado."))