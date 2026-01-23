from django.db import models
from licitaciones.models import Licitacion
from proyectos_E.models import Proyecto_E
from SIA.models import tblProyectos


STATUS_PROYECTOS = (
    (1,"Adjudicado"),
    (2,"Cancelado"),
    (3,"Contratos"),
    (4,"Coordinador"),
    (5,"Desierta"),
    (6,"Diferido"),
    (7,"FMCM"),
    (8,"Fuerzas Internas"),
    (9,"Ingenieria"),
    (10,"IPIS"),
    (11,"ISC"),
    (12,"No Adjudicada"),
    (13,"Pendiente"),
)

class Proyecto_CC(models.Model):
    codigo = models.CharField(max_length=20)
    title = models.TextField(null=True, blank=True)
    seccion = models.CharField(max_length=20, null=True, blank=True)
    coordinador = models.CharField(max_length=200, null=True, blank=True)
    fiscal_year = models.IntegerField(null=True, blank=True, editable=False, 
                                      help_text="Año fiscal calculado a partir del código")
    fecha_entrada = models.DateField(blank=True,null=True)
    fecha_envio_FIO = models.DateField(blank=True,null=True)
    fecha_sol_fondos_aprob = models.DateTimeField(blank=True, null=True)
    fecha_recibo_fondos_aprob = models.DateTimeField(blank=True, null=True)
    asignacion_presup_final = models.FloatField(null=True, blank=True)
    precio_acp = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.IntegerField(choices=STATUS_PROYECTOS, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _calcular_fiscal_year(self):
        if not self.codigo or len(self.codigo) < 5:
            return None
        
        year_str = self.codigo[3:5]
        try:
            year_digits = int(year_str)
            if year_digits > 50:
                return 1900 + year_digits
            else:
                return 2000 + year_digits
        except (ValueError, TypeError):
            return None
        
    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save para calcular y asignar el fiscal_year.
        """
        # Se llama a la lógica de cálculo y se asigna el valor al campo.
        self.fiscal_year = self._calcular_fiscal_year()
        
        # Se llama al método save() original para que guarde el objeto en la BD.
        super().save(*args, **kwargs)

        

    def __str__(self):
        return f"{self.codigo}"
    
class Proyecto_CC_Estimado_Conceptual(models.Model):
    proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE, related_name="proyectos_CC_estimado_conceptual_cc")
    estimado_conceptual = models.ForeignKey(Proyecto_E, on_delete=models.CASCADE, related_name="proyectos_CC_estimado_conceptual_e")

    def __str__(self):
        return f"Proyecto CC: {self.proyecto_cc.codigo} - Estimado Conceptual: {self.estimado_conceptual.codigo}"
    

class Proyecto_CC_Licitacion(models.Model):
    proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE)
    licitacion = models.ForeignKey(Licitacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Proyecto CC: {self.proyecto_cc.codigo} - Licitacion: {self.licitacion.rfq}"
    
class Proyecto_CC_SIA(models.Model):
    proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE)
    sia = models.ForeignKey(tblProyectos, on_delete=models.CASCADE)

    def __str__(self):
        return f"Proyecto CC: {self.proyecto_cc.codigo} - SIA: {self.sia.CodProyecto}"
    
class Proyecto_CC_Secciones_MF(models.Model):
    proyecto_cc = models.ForeignKey(Proyecto_CC, on_delete=models.CASCADE)
    division = models.CharField(max_length=10)
    seccion = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Proyecto CC: {self.proyecto_cc.codigo} - Division: {self.division} - Seccion: {self.seccion}"
    

