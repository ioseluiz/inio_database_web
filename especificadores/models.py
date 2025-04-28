from django.db import models

class Especificador(models.Model):
    nombre = models.CharField(max_length=50)
    iniciales = models.CharField(max_length=5)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre}"
