from django.db import models

from licitaciones.models import Licitacion

class ProyectoCC_Contrato(models.Model):
    pass

class Contrato(models.Model):
    STATUS_CONTRATO = [
        ('OPEN','Open'),
        ('FINALLY CLOSED', 'Finally Closed'),
        ('CLOSED', 'Cosed')
    ]
    numero_contrato = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    rubro = models.CharField(max_length=15,blank=True, null=True)
    tipo_licitacion = models.CharField(max_length=20,blank=True, null=True)
    numero_licitacion = models.CharField(max_length=50,blank=True, null=True)
    licitacion = models.ForeignKey(Licitacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='contratos', verbose_name='Licitacion')
    numero_propuesta_ganadora = models.CharField(max_length=50,blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CONTRATO, db_default='OPEN')
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    fecha_adjudicacion = models.DateTimeField(blank=True, null=True)
    fiscal_year = models.PositiveIntegerField(blank=True, null=True)
    fiscal_month = models.PositiveIntegerField(blank=True, null=True)
    vendor_name = models.CharField(max_length=100,blank=True, null=True)
    monto_contrato_original = models.FloatField(blank=True, null=True)
    monto_pagado = models.FloatField(blank=True, null=True)
    fecha_promesa = models.DateTimeField(blank=True, null=True)
    fecha_maxima_entrega = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Contrato {self.numero_contrato}"
    



