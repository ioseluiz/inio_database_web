import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licitaciones_v2', '0001_initial'),
        ('proyectos_C', '0003_alter_proyecto_cc_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto_CC_Licitacion_V2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='licitaciones_v2.licitacion')),
                ('proyecto_cc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos_C.proyecto_cc')),
            ],
        ),
    ]
