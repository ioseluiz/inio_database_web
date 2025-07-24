from django.db import models

class Proyecto_SE(models.Model):
    codigo = models.CharField(max_length=20)
    title = models.TextField(null=True, blank=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    fecha_sol_fondos = models.DateField()
    fecha_sol_fondos_aprobados = models.DateField()
    comentarios = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.codigo

