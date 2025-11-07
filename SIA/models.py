from django.db import models

class tblProyectos(models.Model):
    CodProyecto = models.CharField(max_length=25, primary_key=True)
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

    HorasTotales = models.FloatField(default=0.0, null=True, blank=True, help_text="Suma total de horas (Regular, Extra, Comp) registradas para este proyecto.")
    horas_estimador = models.FloatField(default=0.0, null=True, blank=True)
    horas_especificador = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return f"{self.CodProyecto}"
    
class tblTransacciones(models.Model):
    Fecha = models.DateTimeField()
    IP = models.CharField(max_length=15)
    CodProyecto = models.ForeignKey(tblProyectos, to_field='CodProyecto', db_column='CodProyecto',on_delete=models.CASCADE, related_name='transacciones')
    HoraRegular = models.FloatField(blank=True, null=True)
    HoraExtra = models.FloatField(blank=True, null=True)
    HoraComp = models.FloatField(blank=True, null=True)
    CodRamo = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Carga de tiempo, SIA: {self.CodProyecto.CodProyecto} por Fecha: {self.Fecha}"
    
    class Meta:
        # Define una clave única compuesta para evitar duplicados si es necesario
        unique_together = ('Fecha', 'IP', 'CodProyecto')
        verbose_name_plural = "tblTransacciones"
    
    

