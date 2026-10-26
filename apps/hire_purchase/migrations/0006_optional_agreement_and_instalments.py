from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("hire_purchase", "0005_data_source_name_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hirepurchaseregistration",
            name="agreement_number",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="The financier's own agreement reference number.",
                max_length=100,
                null=True,
                unique=True,
                verbose_name="Agreement Number",
            ),
        ),
        migrations.AlterField(
            model_name="hirepurchaseregistration",
            name="instalment_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=18,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Instalment Amount",
            ),
        ),
        migrations.AlterField(
            model_name="hirepurchaseregistration",
            name="instalment_day",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Day-of-month (dd) when each instalment falls due.",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(31),
                ],
                verbose_name="Instalment Day",
            ),
        ),
    ]
