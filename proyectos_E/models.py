from django.db import models

class Proyecto_E(models.Model):
    codigo = models.CharField(max_length=25)
    title = models.TextField()
    fecha_entrada = models.DateField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    seccion = models.CharField(max_length=25, blank=True, null=True)
    coordinador = models.CharField(max_length=100, blank=True, null=True)
    bldg = models.CharField(max_length=20, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    fiscal_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo}"
    
    class Meta:
        ordering = ['-created_at']
