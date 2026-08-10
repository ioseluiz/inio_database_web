import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIA', '0002_tblproyectos_horas_especificador_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblUsuarios',
            fields=[
                ('IP', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('NomUsuario', models.CharField(blank=True, max_length=100, null=True)),
                ('Grado', models.CharField(blank=True, max_length=20, null=True)),
                ('Clave', models.CharField(blank=True, max_length=50, null=True)),
                ('Salario', models.FloatField(blank=True, null=True)),
                ('CodRamo', models.CharField(blank=True, max_length=10, null=True)),
                ('Acceso', models.CharField(blank=True, max_length=50, null=True)),
                ('AccesoEstimar', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'tblUsuarios',
            },
        ),
        migrations.AlterField(
            model_name='tbltransacciones',
            name='IP',
            field=models.ForeignKey(
                blank=True,
                db_column='IP',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='transacciones',
                to='SIA.tblusuarios',
                to_field='IP',
            ),
        ),
    ]
