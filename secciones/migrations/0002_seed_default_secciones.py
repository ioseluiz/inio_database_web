from django.db import migrations


DEFAULT_SECCIONES = ["INIC", "INI-PY", "INIG", "INIE", "INIO"]


def seed_secciones(apps, schema_editor):
    Seccion = apps.get_model("secciones", "Seccion")
    for name in DEFAULT_SECCIONES:
        Seccion.objects.update_or_create(name=name, defaults={"is_active": True})


def unseed_secciones(apps, schema_editor):
    Seccion = apps.get_model("secciones", "Seccion")
    Seccion.objects.filter(name__in=DEFAULT_SECCIONES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("secciones", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_secciones, reverse_code=unseed_secciones),
    ]
