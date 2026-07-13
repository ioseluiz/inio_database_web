from django.db import models


class CategoryLicitacion(models.Model):
    """
    Representa las diferentes categorias de licitacion.
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
    Representa un proceso de licitacion de la organizacion.
    """

    ESTADO_LIC_CHOICES = [
        ("Acto Desierto", "Acto Desierto"),
        ("Adjudicacion", "Adjudicacion"),
        ("Anuncio Vencido", "Anuncio Vencido"),
        ("Cancelacion Del Acto", "Cancelacion Del Acto"),
        ("Enmendada", "Enmendada"),
        ("Evaluacion", "Evaluacion"),
        ("En Preparacion", "En Preparacion"),
        ("Abiertas", "Abiertas"),
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


class Propuesta(models.Model):
    """
    Representa una propuesta (bid) presentada por un proponente para una licitacion.
    El campo bid es el identificador externo asignado manualmente.
    """
    bid = models.IntegerField(
        primary_key=True,
        verbose_name="ID de Oferta (Bid)"
    )
    rfq = models.ForeignKey(
        Licitacion,
        on_delete=models.PROTECT,
        related_name='propuestas',
        verbose_name="Licitacion"
    )
    bid_proponente = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Proponente"
    )
    bid_vendor_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nombre del Vendedor"
    )
    bid_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de la Oferta"
    )
    bid_status = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Estado de la Oferta"
    )
    resultado = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Resultado"
    )
    fecha_primer_registro = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de Primer Registro"
    )
    fecha_ultima_actualizacion = models.DateField(
        auto_now=True,
        verbose_name="Fecha de Ultima Actualizacion"
    )
    totalmonto = models.FloatField(
        default=0.0,
        verbose_name="Monto Total"
    )

    class Meta:
        verbose_name = "Propuesta"
        verbose_name_plural = "Propuestas"

    def __str__(self):
        return f"Bid {self.bid} - {self.bid_vendor_name or ''} ({self.rfq_id})"


class PropuestaDetalle(models.Model):
    """
    Representa una linea de detalle dentro de una propuesta.
    """
    bid = models.ForeignKey(
        Propuesta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Propuesta"
    )
    bid_line_no = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Numero de Linea de Oferta"
    )
    bid_line_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Monto de Linea"
    )
    bid_line_number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Numero de Linea"
    )
    bid_line_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Precio de Linea"
    )
    quantity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Cantidad"
    )
    fecha_ultima_actualizacion = models.DateField(
        auto_now=True,
        verbose_name="Fecha de Ultima Actualizacion"
    )

    class Meta:
        unique_together = ('bid', 'bid_line_no')
        verbose_name = "Detalle de Propuesta"
        verbose_name_plural = "Detalles de Propuesta"

    def __str__(self):
        return f"Detalle bid={self.bid_id} linea={self.bid_line_no}"
