import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
import os

import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Importa los modelos definidos
from licitaciones.models import CategoryLicitacion, Licitacion, Enmienda, Propuesta

class Command(BaseCommand):
    help = 'Limpia, importa y actualiza los datos de licitaciones desde un archivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='La ruta al archivo CSV (ej. licitaciones.csv)')

    def _parse_date(self, date_str, row_num, field_name):
        """
        Intenta parsear una cadena de fecha con múltiples formatos y maneja valores nulos.
        """
        # Si la cadena es nula, vacía o 'nan', retorna None inmediatamente.
        if not date_str or pd.isna(date_str):
            return None
        
        date_str = str(date_str)

        # Lista de formatos de fecha a intentar en orden de probabilidad.
        formats_to_try = [
            '%m/%d/%Y %I:%M:%S %p',  # Formato como '3/16/2020 10:55:49 AM'
            '%Y-%m-%d',              # Formato original '2020-03-16'
            '%Y-%m-%d %H:%M:%S',    # Formato con hora de 24h
            '%m/%d/%Y',              # Formato como '3/16/2020'
        ]

        for fmt in formats_to_try:
            try:
                # Intenta convertir la cadena y devuelve solo la parte de la fecha.
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                # Si el formato no coincide, continúa con el siguiente.
                continue

        # Si ningún formato funcionó, se registra el error y se devuelve None.
        self.stdout.write(self.style.ERROR(
            f'    Fila {row_num}: Error al parsear fecha "{field_name}": {date_str}. Formato no reconocido. Establecido a NULL.'
        ))
        return None
    

    def _parse_enmienda_id(self, enmienda_val, row_num):
        """
        Convierte una cadena de enmienda a entero, manejando valores decimales y no numéricos.
        """
        if pd.isna(enmienda_val) or str(enmienda_val).strip() == '':
            return None
        
        try:
            # Intenta convertir a float primero para manejar "1.0", luego a int.
            return int(float(enmienda_val))
        except (ValueError, TypeError):
            # Este bloque se activa si enmienda_val es un texto no numérico como "N/A".
            self.stdout.write(self.style.WARNING(
                f'    Fila {row_num}: Valor de enmienda no es un número válido: "{enmienda_val}". Se omitirá.'
            ))
            return None

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'El archivo CSV no existe en la ruta: {csv_file_path}')
        
        self.stdout.write(self.style.NOTICE(f'Comenzando la importacion desde {csv_file_path}...'))

        try:
            self.stdout.write(self.style.NOTICE('Paso 1: Cargando y limpiando el archivo en memoria...'))
            df = pd.read_csv(csv_file_path)

            # Limpiar saltos de linea
            columnas_a_limpiar = df.columns[:-1]
            for col in columnas_a_limpiar:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.replace(r'[\n\r]+', ' ', regex=True).str.strip()

            # Reemplazar los valores NaN de pandas por None de Python para un manejo consistente
            df = df.astype(object).where(pd.notna(df), None)

            # Convertir el DataFrame limpio a una lista de diccionarios para procesar
            registros_a_procesar = df.to_dict('records')
            self.stdout.write(self.style.SUCCESS('Limpieza en memoria completada. Iniciando procesamiento de filas...'))

        except Exception as e:
            raise CommandError(f"Error al leer o limpiar el archivo CSV con pandas: {e}")
        
        total_rows, created_count, updated_count, skipped_count, error_count = 0, 0, 0, 0, 0
        total_rows = len(registros_a_procesar)

        for row_num, row in enumerate(registros_a_procesar,1):
            self.stdout.write(self.style.HTTP_INFO(f'Procesando fila {row_num}/{total_rows}...'), ending='\r')
            try:
                with transaction.atomic():
                    # -- 1. Procesar CategoryLicitacion ---
                    category_name = row.get('CATEGORY')
                    category_obj = None
                    if category_name:
                        category_obj, created_category = CategoryLicitacion.objects.get_or_create(
                            nombre_categoria=category_name
                        )
                        if created_category:
                            self.stdout.write(self.style.SUCCESS(f' Categoria "{category_name}" creada.'))

                    # -- 2. Procesar Licitacion ---
                    rfq_value = row.get('RFQ')
                    if not rfq_value:
                        self.stdout.write(self.style.WARNING(f'  Fila {row_num}: Saltando fila, "rfq" es nulo o vacio. valor RFQ: {rfq_value}'))
                        skipped_count += 1
                        continue

                    licitacion_data = {
                        'category': category_obj,
                        'rfq_type': row.get('RFQ_TYPE') or None,
                        'gral_desc': row.get('GRAL_DESC') or None,
                        'proc_area': row.get('PROC_AREA') or None,
                    }

                    # Maneja los campos de fecha para Licitacion usando el nuevo método
                    date_fields = {
                        'creation_date': 'CREATION_DATE',
                        'publication_date': 'PUBLICATION_DATE',
                        'closed_date': 'CLOSED_DATE'
                    }
                    for model_field, csv_field in date_fields.items():
                        licitacion_data[model_field] = self._parse_date(row.get(csv_field), row_num, csv_field)

                    # Valida y asigna el campo 'estado_lic'
                    estado_lic_value = row.get('ESTADO_LIC')
                    valid_estados = [choice[0] for choice in Licitacion.ESTADO_LIC_CHOICES]
                    if estado_lic_value in valid_estados:
                        licitacion_data['estado_lic'] = estado_lic_value
                    else:
                        licitacion_data['estado_lic'] = None
                        if estado_lic_value:
                            self.stdout.write(self.style.WARNING(f'    Fila {row_num}: Valor de "estado_lic" "{estado_lic_value}" no es válido. Establecido a NULL.'))

                    licitacion_obj, created_licitacion = Licitacion.objects.get_or_create(
                        rfq=rfq_value,
                        defaults=licitacion_data
                    )

                    if created_licitacion:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f'    Licitación "{rfq_value}" creada.'))
                    else:
                        updated_fields_licitacion = False
                        for key, value in licitacion_data.items():
                            if getattr(licitacion_obj, key) != value:
                                setattr(licitacion_obj, key, value)
                                updated_fields_licitacion = True
                        if updated_fields_licitacion:
                            licitacion_obj.save()
                            updated_count += 1
                            self.stdout.write(self.style.WARNING(f'    Licitación "{rfq_value}" actualizada.'))

                    # -- 3. Procesar Enmienda --
                    enmienda_val_str = row.get('ENMIENDA')
                    fecha_enmienda_str = row.get('FECHA_ENMIENDA')

                    # Solo intentar procesar si el ID de la enmienda no está vacío o es 'nan'.
                    if enmienda_val_str and str(enmienda_val_str).lower() != 'nan':
                        try:
                            enmienda_id_parsed = self._parse_enmienda_id(enmienda_val_str, row_num)
                            fecha_enmienda_parsed = self._parse_date(fecha_enmienda_str, row_num, 'FECHA_ENMIENDA')

                            if enmienda_id_parsed is not None:
                                # Prepara los datos que pueden ser actualizados.
                                enmienda_data = {
                                    'enmienda_desc': row.get('ENMIENDA_DESC') or None,
                                    'fecha_enmienda': fecha_enmienda_parsed,
                                }
                                
                                enmienda_obj, created_enmienda = Enmienda.objects.get_or_create(
                                    licitacion=licitacion_obj,
                                    enmienda_id=enmienda_id_parsed,
                                    defaults=enmienda_data
                                )
                                
                                if created_enmienda:
                                    created_count += 1
                                    self.stdout.write(self.style.SUCCESS(f'    Fila {row_num}: Enmienda {enmienda_id_parsed} creada para licitación "{licitacion_obj.rfq}".'))
                                else:
                                    # --- ¡LÓGICA DE ACTUALIZACIÓN AÑADIDA! ---
                                    # Si la enmienda ya existe, verificamos si hay cambios.
                                    update_needed = False
                                    for field, value in enmienda_data.items():
                                        if getattr(enmienda_obj, field) != value:
                                            setattr(enmienda_obj, field, value)
                                            update_needed = True
                                    
                                    if update_needed:
                                        enmienda_obj.save()
                                        updated_count += 1
                                        self.stdout.write(self.style.WARNING(f'    Fila {row_num}: Enmienda {enmienda_id_parsed} actualizada para licitación "{licitacion_obj.rfq}".'))

                        except (ValueError, TypeError) as e:
                            self.stdout.write(self.style.ERROR(f'    Fila {row_num}: Error al procesar Enmienda: {e}.'))
                            error_count += 1

                    # -- 4. Procesar Propuesta --
                    # Primero, recolectamos todos los datos de la propuesta de la fila
                    bid_proponente_id = row.get('BID_PROPONENTE_ID')
                    bid_line_no = row.get('BID_LINE_NO')
                    bid_vendor_name = row.get('BID_VENDOR_NAME')
                    bid_line_amount_str = row.get('BID_LINE_AMOUNT')

                    # Definimos una bandera para saber si hay datos suficientes para crear un registro
                    hay_datos_de_propuesta = any([
                        bid_proponente_id,
                        bid_line_no,
                        bid_vendor_name,
                        bid_line_amount_str
                    ])

                    if hay_datos_de_propuesta:
                        propuesta_data = {
                            'licitacion': licitacion_obj,
                            'bid_proponente_id': bid_proponente_id or None,
                            'bid_line_no': bid_line_no or None,
                            'bid_vendor_name': bid_vendor_name or None,
                            'rfq_method': row.get('RFQ_METHOD') or None,
                            'resultado': row.get('RESULTADO') or None,
                            'rfq_closed_date': self._parse_date(row.get('RFQ_CLOSED_DATE'), row_num, 'RFQ_CLOSED_DATE'),
                        }
                        
                        try:
                            propuesta_data['bid_line_amount'] = Decimal(bid_line_amount_str) if bid_line_amount_str else None
                        except InvalidOperation:
                            propuesta_data['bid_line_amount'] = None

                        bid_status_value = row.get('BID_STATUS')
                        valid_bid_statuses = [choice[0] for choice in Propuesta.BID_STATUS_CHOICES]
                        propuesta_data['bid_status'] = bid_status_value if bid_status_value in valid_bid_statuses or bid_status_value == '' else None

                        # Solo proceder si tenemos los identificadores únicos para evitar duplicados.
                        if bid_proponente_id and bid_line_no:
                            propuesta_obj, created = Propuesta.objects.get_or_create(
                                licitacion=licitacion_obj,
                                bid_proponente_id=bid_proponente_id,
                                bid_line_no=bid_line_no,
                                defaults=propuesta_data
                            )

                            if created:
                                created_count += 1
                            else:
                                updated_fields = False
                                for key, value in propuesta_data.items():
                                    if getattr(propuesta_obj, key) != value:
                                        setattr(propuesta_obj, key, value)
                                        updated_fields = True
                                if updated_fields:
                                    propuesta_obj.save()
                                    updated_count += 1
                        
                        else:
                            # Si no tenemos los IDs únicos, registramos una advertencia y omitimos para no crear duplicados.
                            self.stdout.write(self.style.WARNING(
                                f'    Fila {row_num}: Se omitió la propuesta para la licitación "{rfq_value}" por falta de BID_PROPONENTE_ID o BID_LINE_NO.'
                            ))
                            skipped_count += 1


                        

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error inesperado al procesar la fila {row_num}: {e}'))
                error_count += 1

        # --- Resumen de la importación ---
        self.stdout.write(self.style.SUCCESS('\n--- Resumen de la importación ---'))
        self.stdout.write(self.style.SUCCESS(f'Filas totales procesadas: {total_rows}'))
        self.stdout.write(self.style.SUCCESS(f'Registros creados: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Registros actualizados: {updated_count}'))
        self.stdout.write(self.style.WARNING(f'Filas saltadas: {skipped_count}'))
        self.stdout.write(self.style.ERROR(f'Errores encontrados: {error_count}'))
        self.stdout.write(self.style.SUCCESS('Importación de datos completada.'))