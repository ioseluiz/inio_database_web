from django.db import models

from proyectos_C.models import Proyecto_CC
from estimadores.models import Estimador

class Proyecto_C_Estimador(models.Model):
    proyecto_c = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE, related_name="proyectos_CC_estimador_relation")
    estimador = models.ForeignKey(Estimador, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return f"{self.proyecto_c.codigo} - {self.estimador.initials}"
    
    class Meta:
        ordering = ['-created_at']
