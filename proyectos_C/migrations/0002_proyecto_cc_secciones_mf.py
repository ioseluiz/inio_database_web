import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos_C', '0001_initial'),
    ]

    operations = [
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
