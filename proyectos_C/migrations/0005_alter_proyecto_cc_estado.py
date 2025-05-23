# Generated by Django 5.2 on 2025-04-28 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos_C', '0004_alter_proyecto_cc_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto_cc',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(1, 'Adjudicado'), (2, 'Cancelado'), (3, 'Contratos'), (4, 'Coordinador'), (5, 'Desierta'), (6, 'Diferido'), (7, 'FMCM'), (8, 'Fuerzas Internas'), (9, 'Ingenieria'), (10, 'IPIS'), (11, 'ISC'), (12, 'No Adjudicada'), (13, 'Pendiente')], null=True),
        ),
    ]
