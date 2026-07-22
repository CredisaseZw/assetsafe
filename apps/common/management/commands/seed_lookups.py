from django.core.management.base import BaseCommand

from apps.common.utils.seed_lookups import seed_system_lookup_options


class Command(BaseCommand):
    help = (
        "Upsert system LookupOption rows (PartyType, BaseAssetType, "
        "AssetCondition, CollateralAssetCategory) from code enums."
    )

    def handle(self, *args, **options):
        count = seed_system_lookup_options()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded system lookup options for {count} categories."
            )
        )
