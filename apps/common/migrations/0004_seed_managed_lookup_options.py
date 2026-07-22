"""Seed managed LookupOption rows (delegates to shared seeder)."""

from django.db import migrations


def seed_lookup_options(apps, schema_editor):
    from apps.common.utils.seed_lookups import seed_system_lookup_options

    seed_system_lookup_options(
        LookupOption=apps.get_model("common", "LookupOption"),
    )


def unseed_lookup_options(apps, schema_editor):
    LookupOption = apps.get_model("common", "LookupOption")
    LookupOption.objects.filter(
        category__in=[
            "PartyType",
            "BaseAssetType",
            "AssetCondition",
            "CollateralAssetCategory",
        ],
        is_system=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0003_managed_lookup_options"),
    ]

    operations = [
        migrations.RunPython(seed_lookup_options, unseed_lookup_options),
    ]
