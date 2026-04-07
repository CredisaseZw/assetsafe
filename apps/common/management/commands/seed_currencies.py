from django.core.management.base import BaseCommand
from apps.common.models import Currency


class Command(BaseCommand):
    """Command to seed default currencies for RentSafe application."""

    help = "Seed default currencies for RentSafe application."

    def handle(self, *args, **kwargs):
        # Define the default currencies with their symbols
        currencies = [
            {
                "code": "USD",
                "name": "United States Dollar",
                "symbol": "$",
            },
            {
                "code": "ZiG",
                "name": "Zimbabwean Dollar",
                "symbol": "Zig",
            },
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
            {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥"},
            {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
            {
                "code": "AUD",
                "name": "Australian Dollar",
                "symbol": "A$",
            },
            {
                "code": "CAD",
                "name": "Canadian Dollar",
                "symbol": "C$",
            },
            {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF"},
            {
                "code": "ZAR",
                "name": "South African Rand",
                "symbol": "R",
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
