from django.db import models

from proyectos_C.models import Proyecto_CC
from especificadores.models import Especificador

class Proyecto_C_Especificador(models.Model):
    proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE, related_name="proyectos_CC_especificador_relation")
    especificador = models.ForeignKey(Especificador, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.proyecto_cc.codigo} - {self.especificador.iniciales}"
    
    class Meta:
        ordering = ['-created_at']
