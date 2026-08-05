import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos_C', '0004_proyecto_cc_licitacion_v2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto_CC_Cronograma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateField(blank=True, null=True)),
                ('entrega_50_porciento', models.DateField(blank=True, null=True)),
                ('entrega_90_porciento', models.DateField(blank=True, null=True)),
                ('entrega_owner', models.DateField(blank=True, null=True)),
                ('proyecto_cc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cronograma', to='proyectos_C.proyecto_cc')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto_CC_Fechas_Actual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio_actual', models.DateField(blank=True, null=True)),
                ('entrega_50_porciento_actual', models.DateField(blank=True, null=True)),
                ('entrega_90_porciento_actual', models.DateField(blank=True, null=True)),
                ('inicio_division_review', models.DateField(blank=True, null=True)),
                ('fin_division_review', models.DateField(blank=True, null=True)),
                ('proyecto_cc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fechas_actual', to='proyectos_C.proyecto_cc')),
            ],
        ),
    ]
