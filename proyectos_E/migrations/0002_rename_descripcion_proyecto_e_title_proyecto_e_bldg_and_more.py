# Generated by Django 5.2 on 2025-04-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos_E', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proyecto_e',
            old_name='descripcion',
            new_name='title',
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='bldg',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='coordinador',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='fecha_entrada',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='fecha_salida',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='fiscal_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto_e',
            name='seccion',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
