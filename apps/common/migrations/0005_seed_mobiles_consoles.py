"""
Ensure BaseAssetType includes Mobiles/Consoles (and other enum rows).

Delegates to the shared seeder so wipe+makemigrations rebuilds do not rely
on hand-maintained row lists in this file.
"""

from django.db import migrations


def seed_lookup_options(apps, schema_editor):
    from apps.common.utils.seed_lookups import seed_system_lookup_options

    seed_system_lookup_options(
        LookupOption=apps.get_model("common", "LookupOption"),
    )


def noop_reverse(apps, schema_editor):
    # Do not delete rows on reverse; staff-custom options may share categories.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0004_seed_managed_lookup_options"),
    ]

    operations = [
        migrations.RunPython(seed_lookup_options, noop_reverse),
    ]
