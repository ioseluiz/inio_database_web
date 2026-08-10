from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .resources import tblProyectos_Resource, tblTransacciones_Resource, tblUsuarios_Resource
from .models import tblProyectos, tblTransacciones, tblUsuarios

@admin.register(tblProyectos)
class SIAAdmin(ImportExportModelAdmin):
    resource_class = tblProyectos_Resource
    list_display = ('CodProyecto','NomProyecto','CodCuenta','CodRamo','CodCliente','Prioridad','TipoCosto','Fiscal','DescProyecto',
                    'FechaRec', 'FechaIni','FechaEIES','FechaEst','FechaReal','IPCoordinador','Abierto')
    search_fields =('CodProyecto','NomProyecto')


@admin.register(tblUsuarios)
class UsuariosAdmin(ImportExportModelAdmin):
    resource_class = tblUsuarios_Resource
    list_display = ('IP', 'NomUsuario', 'Grado', 'CodRamo', 'Salario', 'Acceso', 'AccesoEstimar')
    search_fields = ('IP', 'NomUsuario', 'CodRamo')


@admin.register(tblTransacciones)
class SIATransaccionesAdmin(ImportExportModelAdmin):
    resource_class = tblTransacciones_Resource
    # 1. Se añade un método seguro para mostrar el código del proyecto.
    list_display = ('Fecha', 'get_ip_usuario', 'get_proyecto_codproyecto', 'HoraRegular', 'HoraExtra', 'HoraComp')

    # 2. Se optimiza la consulta para mejorar el rendimiento.
    list_select_related = ('CodProyecto', 'IP')

    # 3. (LA SOLUCIÓN CLAVE) Se cambia el widget del campo ForeignKey.
    #    Esto reemplaza el menú desplegable (que causa el error) por un campo de texto simple.
    raw_id_fields = ('CodProyecto', 'IP')

    search_fields = ('IP__IP', 'IP__NomUsuario', 'CodProyecto__CodProyecto')

    @admin.display(description='Código Proyecto', ordering='CodProyecto__CodProyecto')
    def get_proyecto_codproyecto(self, obj):
        """
        Este método seguro muestra el código del proyecto.
        Si el proyecto relacionado no existe, muestra un mensaje de error
        en lugar de causar que la página falle.
        """
        try:
            # Intenta acceder al código del proyecto relacionado.
            return obj.CodProyecto.CodProyecto
        except tblProyectos.DoesNotExist:
            # Si no lo encuentra, muestra el ID del proyecto "roto" con una advertencia.
            return format_html(
                '<span style="color: red; font-weight: bold;">FALTANTE: {}</span>',
                obj.CodProyecto_id
            )

    @admin.display(description='IP Usuario', ordering='IP__IP')
    def get_ip_usuario(self, obj):
        """
        Muestra el IP del usuario relacionado. Tolera FK huérfana o nula.
        """
        if obj.IP_id is None:
            return format_html('<span style="color: gray;">—</span>')
        try:
            return f"{obj.IP.IP} - {obj.IP.NomUsuario or ''}".strip(" -")
        except tblUsuarios.DoesNotExist:
            return format_html(
                '<span style="color: red; font-weight: bold;">FALTANTE: {}</span>',
                obj.IP_id
            )
