from django.db import models

class Licitacion(models.Model):
    numero = models.CharField(max_length=50)
    fecha_anuncio = models.DateField()
    fecha_cierre = models.DateField()


    def __str__(self):
        return self.numero
