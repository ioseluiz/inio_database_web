"""One-shot: copia Proyecto_CC_Licitacion (v1) a Proyecto_CC_Licitacion_V2 (v2).

Matchea el RFQ del vínculo v1 contra `licitaciones_v2.Licitacion.rfq`. Si la
licitación v2 existe, crea el vínculo v2 con `proyecto_cc` y `licitacion`
correspondientes. Idempotente: no duplica vínculos ya existentes en v2.

Uso:
    python manage.py migrar_puentes_v1_a_v2 [--dry-run]

Motivo: la app tenía dos modelos de puente coexistiendo (v1 legacy y v2 moderno).
Los usuarios crearon 108 vínculos en v1 cuando v2 estaba vacío. Ahora que
`sync_licitaciones_v2` puebla v2 correctamente, el pipeline del dashboard va a
leer del puente v2 — se necesita replicar allí los vínculos históricos.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from licitaciones_v2.models import Licitacion as LicitacionV2
from proyectos_C.models import Proyecto_CC_Licitacion, Proyecto_CC_Licitacion_V2


class Command(BaseCommand):
    help = "Copia vinculos Proyecto_CC_Licitacion (v1) a Proyecto_CC_Licitacion_V2 (v2)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo reporta que se harian, sin escribir.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        modo = "DRY-RUN" if dry_run else "REAL"
        self.stdout.write(self.style.NOTICE(f"Migracion puentes v1 -> v2 (modo={modo})"))

        # Índice de licitaciones v2 por RFQ para lookup O(1)
        lic_v2_por_rfq = {l.rfq: l for l in LicitacionV2.objects.all()}
        self.stdout.write(f"  Licitaciones v2 disponibles: {len(lic_v2_por_rfq):,}")

        # Pares ya existentes en v2 (evitar duplicados). Key = (proyecto_cc_id, licitacion_v2_id)
        pares_v2_existentes = set(
            Proyecto_CC_Licitacion_V2.objects.values_list("proyecto_cc_id", "licitacion_id")
        )
        self.stdout.write(f"  Puentes v2 ya existentes:    {len(pares_v2_existentes):,}")

        v1_qs = Proyecto_CC_Licitacion.objects.select_related("proyecto_cc", "licitacion")
        total_v1 = v1_qs.count()
        self.stdout.write(f"  Puentes v1 a procesar:       {total_v1:,}")

        a_crear = []
        sin_licitacion_v2 = []
        ya_estaban = 0

        for v1 in v1_qs.iterator():
            rfq = getattr(v1.licitacion, "rfq", None)
            if not rfq:
                continue

            lic_v2 = lic_v2_por_rfq.get(rfq)
            if lic_v2 is None:
                sin_licitacion_v2.append((v1.proyecto_cc.codigo, rfq))
                continue

            par = (v1.proyecto_cc_id, lic_v2.id)
            if par in pares_v2_existentes:
                ya_estaban += 1
                continue

            a_crear.append(
                Proyecto_CC_Licitacion_V2(proyecto_cc=v1.proyecto_cc, licitacion=lic_v2)
            )

        if sin_licitacion_v2:
            self.stdout.write(self.style.WARNING(
                f"\n  {len(sin_licitacion_v2)} vinculos v1 sin match en licitaciones v2:"
            ))
            for cod, rfq in sin_licitacion_v2[:20]:
                self.stdout.write(f"    {cod} -> RFQ {rfq}")
            if len(sin_licitacion_v2) > 20:
                self.stdout.write(f"    ... y {len(sin_licitacion_v2) - 20} mas")

        self.stdout.write(self.style.SUCCESS(
            f"\n  A crear en v2:       {len(a_crear):,}"
        ))
        self.stdout.write(f"  Ya estaban en v2:    {ya_estaban:,}")
        self.stdout.write(f"  Sin match:           {len(sin_licitacion_v2):,}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\nDRY-RUN: no se persiste nada."))
            return

        if not a_crear:
            self.stdout.write(self.style.SUCCESS("\nNada que insertar. Migracion completa."))
            return

        with transaction.atomic():
            Proyecto_CC_Licitacion_V2.objects.bulk_create(a_crear, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"\nInsertados {len(a_crear):,} vinculos en Proyecto_CC_Licitacion_V2."
        ))
