from django.core.management.base import BaseCommand
from apps.common.models import Currency


class Command(BaseCommand):
    """Command to seed default currencies for Assetsafe application."""

    help = "Seed default currencies for Assetsafe application."

    def handle(self, *args, **kwargs):
        # Define the default currencies with their symbols
        currencies = [
            {
                "code": "USD",
                "name": "United States Dollar",
                "symbol": "$",
            },
            {
                "code": "Zig",
                "name": "Zimbabwean Gold",
                "symbol": "Zig",
            },
            {
                "code": "Zwl",
                "name": "Zimbabwean Dollar",
                "symbol": "Zwl",
            },
        ]

        for currency in currencies:
            obj, created = Currency.objects.update_or_create(
                code=currency["code"],
                defaults={
                    "name": currency["name"],
                    "symbol": currency["symbol"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {currency['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {currency['code']}"))

        self.stdout.write(
            self.style.SUCCESS("✅ Default currencies seeded successfully.")
        )
