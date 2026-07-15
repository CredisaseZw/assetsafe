"""
Ensure LookupOption.category allows CollateralAssetCategory, then seed rows.

The AlterField for ``category`` choices mirrors the model and is what
``makemigrations`` would regenerate from ``LookupOption.CATEGORY_CHOICES``.
Seed data itself lives in ``apps.common.utils.seed_lookups``.
"""

from django.db import migrations, models


def seed_lookup_options(apps, schema_editor):
    from apps.common.utils.seed_lookups import seed_system_lookup_options

    seed_system_lookup_options(
        LookupOption=apps.get_model("common", "LookupOption"),
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0005_seed_mobiles_consoles"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lookupoption",
            name="category",
            field=models.CharField(
                choices=[
                    ("PartyType", "Party Type"),
                    ("BaseAssetType", "Base Asset Type"),
                    ("AssetCondition", "Asset Condition"),
                    ("CollateralAssetCategory", "Collateral Asset Category"),
                ],
                db_index=True,
                max_length=50,
            ),
        ),
        migrations.RunPython(seed_lookup_options, noop_reverse),
    ]
