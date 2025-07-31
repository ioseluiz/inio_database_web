from django.db import models

class CategoryLicitacion(models.Model):
    """
    Representa las diferentes categorias de licitacion.
    Los valores unicos de la columna 'category' del CSV se mapearan aqui.
    """
    nombre_categoria = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Nombre de la Categoria"
    )

    class Meta:
        verbose_name = "Categoria de Licitacion"
        verbose_name_plural = "Categorias de Licitacion"

    def __str__(self):
        return self.nombre_categoria

class Licitacion(models.Model):
    """
        Representa un proceso de licitacion de la organizacion
    """

    ESTADO_LIC_CHOICES = [
        ("Acto Desierto", "Acto Desierto"),
        ("Adjudicacion", "Adjudicacion"),
        ("Anuncio Vencido", "Anuncio Vencido"),
        ("Cancelacion Del Acto", "Cancelacion Del Acto"), 
        ("Enmendada", "Enmendada"),
        ("Evaluacion", "Evaluacion"),
    ]

    rfq = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Numero de Licitacion (RFQ)"
    )
    category = models.ForeignKey(
        CategoryLicitacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoria"
    )
    rfq_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Tipo de RFQ"
    )

    creation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Creacion"
    )

    publication_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Publicacion"
    )

    closed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Cierre"
    )

    closed_hour = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de Cierre"
    )

    estado_lic = models.CharField(
        max_length=50,
        choices=ESTADO_LIC_CHOICES,
        null=True,
        blank=True,
        verbose_name="Estado de Licitacion"
    )

    gral_desc = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripcion General"
    )

    proc_area = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Licitacion"
        verbose_name_plural = "Licitaciones"

    def __str__(self):
        return self.rfq
    
class Enmienda(models.Model):
    """
        Representa una enmienda para una licitacion especifica
    """
    licitacion = models.ForeignKey(
        Licitacion,
        on_delete=models.CASCADE,
        related_name='enmiendas',
        verbose_name='Licitacion',
    )
    enmienda_id = models.IntegerField(
        verbose_name="ID de Enmienda"
    )

    enmienda_desc = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripcion de Enmienda"
    )

    fecha_enmienda = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Enmienda"
    )

    class Meta:
        # Asegura que la combinacion de licitacion y enmienda_id sea unica
        unique_together = ('licitacion', 'enmienda_id')
        verbose_name = "Enmienda"
        verbose_name_plural = "Enmiendas"

    def __str__(self):
        return f"Enmienda {self.enmienda_id} para {self.licitacion.rfq}"
    
class Propuesta(models.Model):
    """
        Representa cada propuesta hecha por un proponente en una licitacion.
    """
    BID_STATUS_CHOICES = [
        ("CUMPLE", "CUMPLE"),
        ("DESCALIFICADA","DESCALIFICADA"),
        ("INCUMPLE", "INCUMPLE"),
        ("NO CONSIDERADA", "NO CONSIDERADA"),
        ("PROPUESTA REVISADA", "PROPUESTA REVISADA"),
        ("", "Vacío"), # Opción para el string vacío)
    ]

    licitacion = models.ForeignKey(
        Licitacion,
        on_delete=models.CASCADE, # Si la licitación se elimina, sus propuestas también
        related_name='propuestas', # Permite acceder a las propuestas desde la licitación
        verbose_name="Licitación"
    )
    bid_proponente_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="ID Proponente de Oferta"
    )

    bid_line_amount = models.DecimalField(
        max_digits=15, # Número total de dígitos, incluyendo los decimales
        decimal_places=2, # Número de dígitos después del punto decimal
        null=True,
        blank=True,
        verbose_name="Monto de Línea de Oferta"
    )
    bid_line_no = models.CharField( # Considerado CharField ya que podría no ser siempre numérico
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Número de Línea de Oferta"
    )
    bid_status = models.CharField(
        max_length=50,
        choices=BID_STATUS_CHOICES,
        null=True,
        blank=True,
        verbose_name="Estado de Oferta"
    )
    bid_vendor_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nombre de Vendedor de Oferta"
    )
    rfq_closed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Cierre de RFQ (Propuesta)"
    )
    rfq_method = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Método de RFQ (Propuesta)"
    )
    resultado = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Resultado (Propuesta)"
    )

    class Meta:
        # La combinacion de licitacion, proponente y numero de linea de oferta debe ser unica
        unique_together = ('licitacion', 'bid_proponente_id', 'bid_line_no')
        verbose_name = "Propuesta"
        verbose_name_plural = "Propuestas"

    def __str__(self):
        return f"Propuesta de {self.bid_vendor_name} para {self.licitacion.rfq} (Linea {self.bid_line_no})"
