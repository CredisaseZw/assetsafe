"""Management command to import hire_purchase_export.json."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.hire_purchase.services.export_import import (
    import_hire_purchase_export,
    write_failed_export,
)


class Command(BaseCommand):
    help = (
        "Import currencies, companies, individuals, then hire purchases from a "
        "hire_purchase_export.json file, linking parties by fins_number."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            nargs="?",
            default=None,
            help=(
                "Path to hire_purchase_export.json "
                "(default: <project>/designs/hire_purchase_export.json)"
            ),
        )
        parser.add_argument(
            "--failed-output",
            default=None,
            help="Path for failed records JSON (default: <input>.failed.json)",
        )
        parser.add_argument(
            "--progress-every",
            type=int,
            default=1000,
            help="Print progress after this many records (default: 100)",
        )

    def handle(self, *args, **options):
        path_option = options.get("path")
        if path_option:
            path = Path(path_option)
        else:
            path = Path(settings.BASE_DIR) / "designs" / "hire_purchase_export.json"

        if not path.is_file():
            raise CommandError(f"Export file not found: {path}")

        self.stdout.write(f"Importing from {path} …")
        result = import_hire_purchase_export(
            path,
            stdout=self.stdout,
            progress_every=options["progress_every"],
        )
        failed_output = (
            Path(options["failed_output"])
            if options["failed_output"]
            else path.with_suffix(".failed.json")
        )
        write_failed_export(failed_output, result)
        self.stdout.write(
            self.style.SUCCESS(
                "Done. "
                f"HP created={result.hire_purchases_created}, "
                f"updated={result.hire_purchases_updated}, "
                f"excluded={result.hire_purchases_excluded}, "
                f"start_defaulted={result.hire_purchases_start_defaulted}, "
                f"end_randomized={result.hire_purchases_end_randomized}, "
                f"skipped={len(result.skipped)}, "
                f"errors={len(result.errors)}, "
                f"failed_file={failed_output}"
            )
        )
