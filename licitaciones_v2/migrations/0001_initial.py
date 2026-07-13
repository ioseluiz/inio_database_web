import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CategoryLicitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=255, unique=True, verbose_name='Nombre de la Categoria')),
            ],
            options={
                'verbose_name': 'Categoria de Licitacion',
                'verbose_name_plural': 'Categorias de Licitacion',
            },
        ),
        migrations.CreateModel(
            name='Licitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfq', models.CharField(max_length=255, unique=True, verbose_name='Numero de Licitacion (RFQ)')),
                ('rfq_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tipo de RFQ')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Creacion')),
                ('publication_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Publicacion')),
                ('closed_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Cierre')),
                ('closed_hour', models.TimeField(blank=True, null=True, verbose_name='Hora de Cierre')),
                ('estado_lic', models.CharField(blank=True, choices=[('Acto Desierto', 'Acto Desierto'), ('Adjudicacion', 'Adjudicacion'), ('Anuncio Vencido', 'Anuncio Vencido'), ('Cancelacion Del Acto', 'Cancelacion Del Acto'), ('Enmendada', 'Enmendada'), ('Evaluacion', 'Evaluacion'), ('En Preparacion', 'En Preparacion'), ('Abiertas', 'Abiertas')], max_length=50, null=True, verbose_name='Estado de Licitacion')),
                ('gral_desc', models.TextField(blank=True, null=True, verbose_name='Descripcion General')),
                ('proc_area', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='licitaciones_v2.categorylicitacion', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Licitacion',
                'verbose_name_plural': 'Licitaciones',
            },
        ),
        migrations.CreateModel(
            name='Propuesta',
            fields=[
                ('bid', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID de Oferta (Bid)')),
                ('bid_proponente', models.CharField(blank=True, max_length=255, null=True, verbose_name='Proponente')),
                ('bid_vendor_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre del Vendedor')),
                ('bid_date', models.DateField(blank=True, null=True, verbose_name='Fecha de la Oferta')),
                ('bid_status', models.CharField(blank=True, max_length=255, null=True, verbose_name='Estado de la Oferta')),
                ('resultado', models.CharField(blank=True, max_length=255, null=True, verbose_name='Resultado')),
                ('fecha_primer_registro', models.DateField(auto_now_add=True, verbose_name='Fecha de Primer Registro')),
                ('fecha_ultima_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de Ultima Actualizacion')),
                ('totalmonto', models.FloatField(default=0.0, verbose_name='Monto Total')),
                ('rfq', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='propuestas', to='licitaciones_v2.licitacion', verbose_name='Licitacion')),
            ],
            options={
                'verbose_name': 'Propuesta',
                'verbose_name_plural': 'Propuestas',
            },
        ),
        migrations.CreateModel(
            name='PropuestaDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_line_no', models.IntegerField(blank=True, null=True, verbose_name='Numero de Linea de Oferta')),
                ('bid_line_amount', models.FloatField(blank=True, null=True, verbose_name='Monto de Linea')),
                ('bid_line_number', models.IntegerField(blank=True, null=True, verbose_name='Numero de Linea')),
                ('bid_line_price', models.FloatField(blank=True, null=True, verbose_name='Precio de Linea')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Cantidad')),
                ('fecha_ultima_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de Ultima Actualizacion')),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='licitaciones_v2.propuesta', verbose_name='Propuesta')),
            ],
            options={
                'verbose_name': 'Detalle de Propuesta',
                'verbose_name_plural': 'Detalles de Propuesta',
                'unique_together': {('bid', 'bid_line_no')},
            },
        ),
    ]
