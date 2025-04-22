from django.db import models

from proyectos_E.models import Proyecto_E
from estimadores.models import Estimador

class Proyecto_E_Estimador(models.Model):
    proyecto_e = models.ForeignKey(Proyecto_E, on_delete=models.CASCADE)
    estimador = models.ForeignKey(Estimador, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.proyecto_e.codigo} - {self.estimador.initials}"
    
    class Meta:
        ordering = ['-created_at']
    


