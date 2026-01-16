from django.db import models

from SIA.models import tblProyectos

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
    asignacion_presup = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo}"
    
    class Meta:
        ordering = ['-created_at']


class HorasApoyo(models.Model):
    proyecto_e = models.ForeignKey(Proyecto_E, on_delete=models.CASCADE, related_name='horas_de_apoyo')
    revision = models.CharField(max_length=10, null=True, blank=True)
    hr_diseno_inic_ar = models.FloatField(null=True, blank=True)
    hr_diseno_inic_ic = models.FloatField(null=True, blank=True)
    hr_diseno_inic_ie = models.FloatField(null=True, blank=True)
    hr_diseno_inic_ih = models.FloatField(null=True, blank=True)
    hr_diseno_inie_dm = models.FloatField(null=True, blank=True)
    hr_diseno_inie_ee = models.FloatField(null=True, blank=True)
    hr_diseno_inie_sm = models.FloatField(null=True, blank=True)
    hr_diseno_inig_ig = models.FloatField(null=True, blank=True)
    hr_diseno_inig_pe = models.FloatField(null=True, blank=True)
    hr_diseno_inio_ce = models.FloatField(null=True, blank=True)
    hr_diseno_inio_es = models.FloatField(null=True, blank=True)
    hr_diseno_init = models.FloatField(null=True, blank=True)
    
    hr_apoyo_inic_ar = models.FloatField(null=True, blank=True)
    hr_apoyo_inic_ic = models.FloatField(null=True, blank=True)
    hr_apoyo_inic_ie = models.FloatField(null=True, blank=True)
    hr_apoyo_inic_ih = models.FloatField(null=True, blank=True)
    hr_apoyo_inie_dm = models.FloatField(null=True, blank=True)
    hr_apoyo_inie_ee = models.FloatField(null=True, blank=True)
    hr_apoyo_inie_sm = models.FloatField(null=True, blank=True)
    hr_apoyo_inig_ig = models.FloatField(null=True, blank=True)
    hr_apoyo_inig_pe = models.FloatField(null=True, blank=True)
    hr_apoyo_inio_ce = models.FloatField(null=True, blank=True)
    hr_apoyo_inio_es = models.FloatField(null=True, blank=True)
    hr_apoyo_init = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.proyecto_e.codigo}"
    
    class Meta:
        ordering = ['-created_at']


class Proyecto_E_SIA(models.Model):
    proyecto_e = models.ForeignKey(Proyecto_E, on_delete=models.CASCADE)
    sia = models.ForeignKey(tblProyectos, on_delete=models.CASCADE)

    def __str__(self):
        return f"Proyecto E: {self.proyecto_e.codigo} - SIA: {self.sia.CodProyecto}"


