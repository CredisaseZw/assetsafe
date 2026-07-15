# Schema: asset_category + free-text asset_type.
# On wipe+makemigrations, recreate from models; RunPython only for existing DBs.

from django.db import migrations, models


def copy_asset_type_to_category(apps, schema_editor):
    HirePurchaseRegistration = apps.get_model(
        "hire_purchase", "HirePurchaseRegistration"
    )
    for row in HirePurchaseRegistration.objects.all().iterator():
        if row.asset_type and not getattr(row, "asset_category", None):
            row.asset_category = row.asset_type
            row.asset_type = ""
            row.save(update_fields=["asset_category", "asset_type"])


def reverse_copy(apps, schema_editor):
    HirePurchaseRegistration = apps.get_model(
        "hire_purchase", "HirePurchaseRegistration"
    )
    for row in HirePurchaseRegistration.objects.all().iterator():
        if row.asset_category and not row.asset_type:
            row.asset_type = row.asset_category
            row.save(update_fields=["asset_type"])


class Migration(migrations.Migration):
    dependencies = [
        ("hire_purchase", "0003_managed_lookup_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="hirepurchaseregistration",
            name="asset_category",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="High-level category from managed base asset types.",
                max_length=50,
                verbose_name="Asset Category",
            ),
        ),
        migrations.AlterField(
            model_name="hirepurchaseregistration",
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
            model_name="hirepurchaseregistration",
            name="asset_category",
            field=models.CharField(
                db_index=True,
                help_text="High-level category from managed base asset types.",
                max_length=50,
                verbose_name="Asset Category",
            ),
        ),
    ]
