from django.db import models

from proyectos_C.models import Proyecto_CC


class tblProyectos(models.Model):
    CodProyecto = models.CharField(max_length=25)
    NomProyecto = models.TextField(blank=True, null=True)
    CodCuenta = models.PositiveIntegerField(blank=True, null=True)
    CodRamo = models.CharField(max_length=10,blank=True, null=True)
    CodCliente = models.CharField(max_length=20,blank=True, null=True)
    Prioridad = models.PositiveIntegerField(blank=True, null=True)
    TipoCosto = models.CharField(max_length=5,blank=True, null=True)
    Fiscal = models.PositiveIntegerField(blank=True, null=True)
    DescProyecto = models.TextField(blank=True, null=True)
    FechaRec = models.DateTimeField(blank=True, null=True)
    FechaIni = models.DateTimeField(blank=True, null=True)
    FechaEIES = models.DateTimeField(blank=True, null=True)
    FechaEst = models.DateTimeField(blank=True, null=True)
    FechaReal = models.DateTimeField(blank=True, null=True)
    IPCoordinador = models.CharField(max_length=50,blank=True, null=True)
    Abierto = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"SIA No.: {self.CodProyecto}"
    
# class tblTransacciones(models.Model)
    


    # class SIA_Proyecto_CC(models.Model):
    #     cod_proyecto = models.ForeignKey(SIA, on_delete=models.CASCADE, related_name="sia_proyecto_cc_relation")
    #     proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE, related_name="proyecto_cc_sia_relation")

    #     def __str__(self):
    #         return f"Proyecto CC: {self.proyecto_cc} - SIA: {self.cod_proyecto}"
    
    

