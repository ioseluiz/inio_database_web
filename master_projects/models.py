from django.db import models

from proyectos_C.models import Proyecto_CC

ESTADO_PROYECTOS = (
    (1,"SIN INICIAR"),
    (2,"EN PROCESO"),
    (3,"ENTREGADO"),
    
)

class MasterProject(models.Model):
    unidad_solicitante = models.CharField(max_length=5)
    nip = models.CharField(max_length=10, null=True, blank=True)
    proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE, related_name="master_proyectos")
    fecha_estimada_entrega_owner = models.DateField(blank=True, null=True)
    fiscal_year = models.PositiveIntegerField()
    comentarios = models.TextField(null=True, blank=True)
    estado = models.IntegerField(choices=ESTADO_PROYECTOS, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proyecto Master: {self.proyecto_cc.codigo} , Año Fiscal: {self.fiscal_year}"
    
