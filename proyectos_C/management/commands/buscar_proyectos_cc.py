import re
from django.core.management.base import BaseCommand
from SIA.models import tblProyectos
from proyectos_C.models import Proyecto_CC, Proyecto_CC_SIA

class Command(BaseCommand):
    """
        Este comando de Django busca proyectos que contengan un codigo de proyecto CC (CC-XX-XX)
        en el nombre del proyecto (NomProyecto)
    """
    help = 'Busca y extrae codigos de proyectos CC desde NomProyecto en tblProyectos'

    def handle(self, *args, **options):

        # Expresión regular para encontrar el patrón "CC-" seguido de dos guiones y dígitos.
        # \d{2} coincide exactamente con dos dígitos.
        patron_cc = re.compile(r'CC-\d{2}-\d{2}', re.IGNORECASE)

        # Contadores para el resumen final
        nuevos_registros = 0
        registros_existentes = 0
        cc_no_encontrados = 0

        # Obtenemos todos los registros de la tabla tblProyectos.
        proyectos = tblProyectos.objects.all()

        for proyecto in proyectos:
                # Nos aseguramos de que NomProyecto no sea None y sea una cadena de texto.
                if proyecto.NomProyecto:
                    # Buscamos todas las coincidencias del patrón en el nombre del proyecto.
                    coincidencias = patron_cc.findall(proyecto.NomProyecto)
                    
                    # Si se encontraron una o más coincidencias.
                    if coincidencias:
                        # Por cada código CC encontrado, creamos un diccionario y lo añadimos a la lista.
                        for codigo_cc in coincidencias:
                            try:
                                # 1. Intentar obtener el objecto Proyecto_CC. No se crearan nuevos
                                proyecto_cc_obj = Proyecto_CC.objects.get(codigo=codigo_cc.upper())

                                # 2. Si se encontro, crar la relacion en Proyecto_CC_SIA si no existe.
                                # Usamos get_or_create para evitar duplicados en la tabla de relacion.
                                relacion, rel_created = Proyecto_CC_SIA.objects.get_or_create(
                                  proyecto_cc=proyecto_cc_obj,
                                  sia=proyecto
                                )
                                if rel_created:
                                    nuevos_registros += 1
                                    self.stdout.write(f"  -> Relación creada: SIA '{proyecto.CodProyecto}' -> CC '{proyecto_cc_obj.codigo}'")
                                else:
                                    registros_existentes += 1
                                    self.stdout.write(self.style.NOTICE(f"  -> Relación ya existente: SIA '{proyecto.CodProyecto}' -> CC '{proyecto_cc_obj.codigo}'"))
                            except Proyecto_CC.DoesNotExist:
                                # Si el Proyecto_CC no existe en la base de datos, se informa y se ignora.
                                cc_no_encontrados += 1
                                self.stdout.write(self.style.WARNING(f"  -> Proyecto_CC '{codigo_cc.upper()}' no encontrado. Se omite la relación."))
                                continue

        # Imprimir un resumen final de la operación.
        self.stdout.write(self.style.SUCCESS('\n--- Proceso Finalizado ---'))
        self.stdout.write(f"Nuevas relaciones creadas: {nuevos_registros}")
        self.stdout.write(f"Relaciones que ya existían: {registros_existentes}")
        self.stdout.write(self.style.WARNING(f"Códigos de CC encontrados en SIA pero no en Proyecto_CC: {cc_no_encontrados}"))