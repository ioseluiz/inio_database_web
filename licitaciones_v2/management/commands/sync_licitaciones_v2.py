import json
from pathlib import Path

import tablib
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from licitaciones_v2.models import CategoryLicitacion
from licitaciones_v2.resources import (
    LicitacionResource,
    PropuestaDetalleResource,
    PropuestaResource,
)


CSV_LICITACIONES = "licitaciones_v2.csv"
CSV_PROPUESTAS = "propuestas_v2.csv"
CSV_DETALLE = "propuesta_detalle_v2.csv"


class Command(BaseCommand):
    """
    Sincroniza licitaciones_v2 desde un directorio con 3 CSVs producidos por
    export_para_prod.py en el pipeline local de ordenar_licitaciones.

    Uso:
        python manage.py sync_licitaciones_v2 <inbox_dir> [--dry-run]
    """

    help = "Sincroniza Licitacion + Propuesta + PropuestaDetalle desde CSVs en un directorio."

    def add_arguments(self, parser):
        parser.add_argument(
            "inbox_dir",
            type=str,
            help="Directorio con los 3 CSVs de sync (licitaciones_v2.csv, propuestas_v2.csv, propuesta_detalle_v2.csv)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simula el import sin escribir en la BD. Reporta counts esperados.",
        )

    def handle(self, *args, **options):
        inbox = Path(options["inbox_dir"])
        dry_run = options["dry_run"]

        if not inbox.is_dir():
            raise CommandError(f"El directorio no existe: {inbox}")

        for csv_name in (CSV_LICITACIONES, CSV_PROPUESTAS, CSV_DETALLE):
            if not (inbox / csv_name).is_file():
                raise CommandError(f"Falta el archivo esperado: {inbox / csv_name}")

        mode_label = "DRY-RUN" if dry_run else "REAL"
        self.stdout.write(self.style.NOTICE(f"Sync licitaciones_v2 modo={mode_label} desde {inbox}"))

        summary = {}

        try:
            summary["categorias"] = self._ensure_categories(inbox / CSV_LICITACIONES, dry_run)
            summary["licitacion"] = self._import_csv(
                inbox / CSV_LICITACIONES, LicitacionResource(), dry_run, "Licitacion"
            )
            summary["propuesta"] = self._import_csv(
                inbox / CSV_PROPUESTAS, PropuestaResource(), dry_run, "Propuesta"
            )
            summary["detalle"] = self._import_csv(
                inbox / CSV_DETALLE, PropuestaDetalleResource(), dry_run, "PropuestaDetalle"
            )
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Sync abortado: {exc}"))
            raise CommandError(str(exc))

        self.stdout.write(self.style.SUCCESS("Sync completado."))
        self.stdout.write("SUMMARY_JSON:" + json.dumps(summary))

    def _ensure_categories(self, licitaciones_csv, dry_run):
        """
        Pre-crea CategoryLicitacion desde la columna `category` del CSV de licitaciones.
        El LicitacionResource usa ForeignKeyWidget que exige que la categoria exista.
        """
        with open(licitaciones_csv, "r", encoding="utf-8-sig", newline="") as fh:
            dataset = tablib.Dataset().load(fh.read(), format="csv")

        if "category" not in dataset.headers:
            return {"new": 0, "existing": 0}

        raw = [row[dataset.headers.index("category")] for row in dataset]
        unique_names = sorted({(v or "").strip() for v in raw if v and str(v).strip()})

        if not unique_names:
            return {"new": 0, "existing": 0}

        existing = set(
            CategoryLicitacion.objects.filter(nombre_categoria__in=unique_names).values_list(
                "nombre_categoria", flat=True
            )
        )
        missing = [n for n in unique_names if n not in existing]

        if dry_run:
            return {"new": len(missing), "existing": len(existing)}

        with transaction.atomic():
            CategoryLicitacion.objects.bulk_create(
                [CategoryLicitacion(nombre_categoria=n) for n in missing],
                ignore_conflicts=True,
            )

        return {"new": len(missing), "existing": len(existing)}

    def _import_csv(self, csv_path, resource, dry_run, label):
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as fh:
            dataset = tablib.Dataset().load(fh.read(), format="csv")

        self.stdout.write(f"  {label}: {len(dataset)} filas en {csv_path.name}")

        result = resource.import_data(
            dataset,
            dry_run=dry_run,
            raise_errors=False,
            use_transactions=True,
            collect_failed_rows=True,
        )

        counts = dict(result.totals)

        if result.has_errors() or result.has_validation_errors():
            error_rows = []
            for row_result in result.row_errors():
                row_num, errors = row_result
                for err in errors:
                    error_rows.append({"row": row_num, "error": str(err.error)})
                    if len(error_rows) >= 10:
                        break
                if len(error_rows) >= 10:
                    break
            counts["error_samples"] = error_rows
            self.stderr.write(self.style.ERROR(f"  {label}: errores detectados"))
            for sample in error_rows:
                self.stderr.write(self.style.ERROR(f"    fila {sample['row']}: {sample['error']}"))
            raise RuntimeError(f"{label} import fallo con {len(error_rows)}+ errores")

        summary_line = " ".join(f"{k}={v}" for k, v in counts.items())
        self.stdout.write(self.style.SUCCESS(f"  {label}: {summary_line}"))
        return counts
