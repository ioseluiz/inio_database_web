import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Importa los modelos definidos
from licitaciones.models import CategoryLicitacion, Licitacion, Enmienda, Propuesta

class Command(BaseCommand):
    help = 'Importa y actualiza datos de licitaciones desde un archivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='La ruta al archivo CSV (ej. licitaciones.csv)')

    def _parse_date(self, date_str, row_num, field_name):
        """
        Intenta parsear una cadena de fecha con múltiples formatos y maneja valores nulos.
        """
        # Si la cadena es nula, vacía o 'nan', retorna None inmediatamente.
        if not date_str or date_str.lower() == 'nan':
            return None

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
    

    def _parse_enmienda_id(self, enmienda_str, row_num):
        """
        Convierte una cadena de enmienda a entero, manejando valores decimales.
        """
        if not enmienda_str or enmienda_str.lower() == 'nan':
            return None
        
        try:
            # Primero convertir a float para manejar valores como '1.0'
            float_val = float(enmienda_str)
            # Luego convertir a entero
            int_val = int(float_val)
            return int_val
        except (ValueError, TypeError) as e:
            self.stdout.write(self.style.ERROR(
                f'    Fila {row_num}: Error al parsear enmienda_id "{enmienda_str}": {e}. Establecido a NULL.'
            ))
            return None


    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'El archivo CSV no existe en la ruta: {csv_file_path}')
        
        self.stdout.write(self.style.NOTICE(f'Comenzando la importacion desde {csv_file_path}...'))

        total_rows, created_count, updated_count, skipped_count, error_count = 0, 0, 0, 0, 0

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 1):
                total_rows += 1
                self.stdout.write(self.style.HTTP_INFO(f'Procesando fila {row_num}...'), ending='\r')

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

                        if enmienda_val_str and fecha_enmienda_str:
                            try:
                                enmienda_id_parsed = self._parse_enmienda_id(enmienda_val_str, row_num)
                                if enmienda_id_parsed is None:
                                    # Si no se pudo parsear el ID, continúa con la siguiente fila
                                    continue
    
                                enmienda_data = {
                                    'licitacion': licitacion_obj,
                                    'enmienda_id': enmienda_id_parsed,
                                    'enmienda_desc': row.get('ENMIENDA_DESC') or None,
                                    'fecha_enmienda': self._parse_date(fecha_enmienda_str, row_num, 'FECHA_ENMIENDA'),
                                }
                                
                                # Solo procesa si la fecha de enmienda fue válida
                                if enmienda_data['fecha_enmienda']:
                                    enmienda_obj, created_enmienda = Enmienda.objects.get_or_create(
                                        licitacion=licitacion_obj,
                                        enmienda_id=enmienda_data['enmienda_id'],
                                        defaults=enmienda_data
                                    )
                                    if created_enmienda:
                                        created_count += 1
                                    # (Lógica de actualización de enmienda aquí...)

                            except (ValueError, TypeError) as e:
                                self.stdout.write(self.style.ERROR(f'    Fila {row_num}: Error al procesar Enmienda: {e}.'))
                                error_count += 1

                        # -- 4. Procesar Propuesta --
                        bid_proponente_id = row.get('BID_PROPONENTE_ID')
                        bid_line_no = row.get('BID_LINE_NO')

                        if bid_proponente_id and bid_line_no:
                            propuesta_data = {
                                'licitacion': licitacion_obj,
                                'bid_proponente_id': bid_proponente_id,
                                'bid_line_no': bid_line_no,
                                # ... otros campos ...
                            }

                            # Maneja fechas para Propuesta usando el nuevo método
                            propuesta_date_fields = {
                                'bid_date': 'bid_date',
                                'rfq_closed_date': 'rfq_closed_date',
                            }
                            for model_field, csv_field in propuesta_date_fields.items():
                                propuesta_data[model_field] = self._parse_date(row.get(csv_field), row_num, csv_field)

                            # (Resto de la lógica para procesar Propuesta)
                            # ...

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