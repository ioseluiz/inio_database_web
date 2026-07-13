import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licitaciones_v2', '0001_initial'),
        ('proyectos_C', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto_cc',
            name='estado',
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, 'Adjudicado'),
                    (2, 'Cancelado'),
                    (3, 'Contratos'),
                    (4, 'Coordinador'),
                    (5, 'Desierta'),
                    (6, 'Diferido'),
                    (7, 'FMCM'),
                    (8, 'Fuerzas Internas'),
                    (9, 'Ingenieria'),
                    (10, 'IPIS'),
                    (11, 'ISC'),
                    (12, 'No Adjudicada'),
                    (13, 'Pendiente'),
                    (14, 'Dueño'),
                ],
                null=True,
            ),
        ),
        migrations.CreateModel(
            name='Proyecto_CC_Licitacion_V2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='licitaciones_v2.licitacion')),
                ('proyecto_cc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos_C.proyecto_cc')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto_CC_Secciones_MF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=10)),
                ('seccion', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('proyecto_cc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos_C.proyecto_cc')),
            ],
        ),
    ]
