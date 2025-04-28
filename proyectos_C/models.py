from django.db import models

STATUS_PROYECTOS = (
    (1,"Adjudicado"),
    (2,"Cancelado"),
    (3,"Contratos"),
    (4,"Coordinador"),
    (5,"Desierta"),
    (6,"Diferido"),
    (7,"FMCM"),
    (8,"Fuerzas Internas"),
    (9,"Ingenieria"),
    (10,"IPIS"),
    (11,"ISC"),
    (12,"No Adjudicada"),
    (13,"Pendiente"),
)

class Proyecto_CC(models.Model):
    codigo = models.CharField(max_length=20)
    title = models.TextField(null=True, blank=True)
    seccion = models.CharField(max_length=20, null=True, blank=True)
    coordinador = models.CharField(max_length=200, null=True, blank=True)
    fecha_entrada = models.DateField(blank=True,null=True)
    fecha_envio_FIO = models.DateField(blank=True,null=True)
    fecha_sol_fondos_aprob = models.DateTimeField(blank=True, null=True)
    fecha_recibo_fondos_aprob = models.DateTimeField(blank=True, null=True)
    asignacion_presup_final = models.FloatField(null=True, blank=True)
    precio_acp = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.IntegerField(choices=STATUS_PROYECTOS, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo}"
