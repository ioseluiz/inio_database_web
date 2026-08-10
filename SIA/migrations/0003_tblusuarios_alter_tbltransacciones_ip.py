import django.db.models.deletion
from django.db import migrations, models


def populate_tblusuarios_from_transacciones(apps, schema_editor):
    """
    Antes de convertir tblTransacciones.IP en FK, aseguramos que todos los IPs
    ya presentes en tblTransacciones existan en tblUsuarios. Si no, la creacion
    de la constraint FK falla con IntegrityError.

    Los IPs se insertan con los campos opcionales en NULL. Un sync posterior
    contra la fuente real (import_transacciones/import_SIA) rellenara los
    demas atributos.
    """
    tblTransacciones = apps.get_model("SIA", "tblTransacciones")
    tblUsuarios = apps.get_model("SIA", "tblUsuarios")

    ips = (
        tblTransacciones.objects.exclude(IP__isnull=True)
        .exclude(IP__exact="")
        .values_list("IP", flat=True)
        .distinct()
    )

    tblUsuarios.objects.bulk_create(
        [tblUsuarios(IP=ip) for ip in ips],
        ignore_conflicts=True,
    )


def reverse_noop(apps, schema_editor):
    """
    Reversa no-op: el rollback de la migracion completa dropea la tabla
    tblUsuarios via CreateModel-reverse, lo cual borra estas filas por si mismo.
    """
    pass


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
        migrations.RunPython(
            populate_tblusuarios_from_transacciones,
            reverse_code=reverse_noop,
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
