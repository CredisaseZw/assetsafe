# Generated migration for AuditLog model

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_customuser_position"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(auto_now_add=True, null=True, blank=True),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, null=True, blank=True),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "action",
                    models.CharField(
                        help_text="Description of the action performed.",
                        max_length=255,
                    ),
                ),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        blank=True,
                        help_text="IP address from which the action originated.",
                        null=True,
                    ),
                ),
                (
                    "user_agent",
                    models.TextField(
                        blank=True, help_text="User agent string of the client."
                    ),
                ),
                (
                    "details",
                    models.JSONField(
                        blank=True,
                        help_text="Detailed context of the action (e.g., changed fields, old/new values, request data).",
                        null=True,
                    ),
                ),
                (
                    "resource_type",
                    models.CharField(
                        blank=True,
                        help_text="Type of resource affected (e.g., 'User', 'Company', 'Property').",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "resource_id",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="ID of the resource affected.",
                        null=True,
                    ),
                ),
                (
                    "success",
                    models.BooleanField(
                        default=True,
                        help_text="Whether the action was successful.",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="auditlog_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="auditlog_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Audit Log",
                "verbose_name_plural": "Audit Logs",
                "ordering": ["-timestamp"],
                "app_label": "users",
            },
        ),
    ]
