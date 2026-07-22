# Generated for asset_category + free-text asset_type.
#
# On a future wipe+makemigrations rebuild, recreate schema from models only.
# This RunPython backfill is only needed when converting existing DBs that
# already stored category values in ``asset_type``.

from django.db import migrations, models


def copy_asset_type_to_category(apps, schema_editor):
    CollateralRegistration = apps.get_model("collateral", "CollateralRegistration")
    for row in CollateralRegistration.objects.all().iterator():
        if row.asset_type and not getattr(row, "asset_category", None):
            row.asset_category = row.asset_type
            row.asset_type = ""
            row.save(update_fields=["asset_category", "asset_type"])


def reverse_copy(apps, schema_editor):
    CollateralRegistration = apps.get_model("collateral", "CollateralRegistration")
    for row in CollateralRegistration.objects.all().iterator():
        if row.asset_category and not row.asset_type:
            row.asset_type = row.asset_category
            row.save(update_fields=["asset_type"])


class Migration(migrations.Migration):
    dependencies = [
        ("collateral", "0004_managed_lookup_options"),
        ("common", "0006_seed_collateral_asset_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="collateralregistration",
            name="asset_category",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="High-level category from managed collateral asset categories.",
                max_length=50,
                verbose_name="Asset Category",
            ),
        ),
        migrations.AlterField(
            model_name="collateralregistration",
            name="asset_type",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Free-text subtype describing the asset within its category.",
                max_length=100,
                verbose_name="Asset Type",
            ),
        ),
        migrations.RunPython(copy_asset_type_to_category, reverse_copy),
        migrations.AlterField(
            model_name="collateralregistration",
            name="asset_category",
            field=models.CharField(
                db_index=True,
                help_text="High-level category from managed collateral asset categories.",
                max_length=50,
                verbose_name="Asset Category",
            ),
        ),
    ]
