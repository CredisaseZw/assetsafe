from django.core.management.base import BaseCommand
from apps.accounting.models.models import Currency


class Command(BaseCommand):
    """Command to seed default currencies for RentSafe application."""
    help = "Seed default currencies for RentSafe application."

    def handle(self, *args, **kwargs):
        # Define the default currencies with their symbols
        currencies = [
            {"currency_code": "USD", "currency_name": "United States Dollar", "symbol": "$"},
            {"currency_code": "ZiG", "currency_name": "Zimbabwean Dollar", "symbol": "Zig"},
            {"currency_code": "EUR", "currency_name": "Euro", "symbol": "€"},
            {"currency_code": "GBP", "currency_name": "British Pound", "symbol": "£"},
            {"currency_code": "JPY", "currency_name": "Japanese Yen", "symbol": "¥"},
            {"currency_code": "CNY", "currency_name": "Chinese Yuan", "symbol": "¥"},
            {"currency_code": "INR", "currency_name": "Indian Rupee", "symbol": "₹"},
            {"currency_code": "AUD", "currency_name": "Australian Dollar", "symbol": "A$"},
            {"currency_code": "CAD", "currency_name": "Canadian Dollar", "symbol": "C$"},
            {"currency_code": "CHF", "currency_name": "Swiss Franc", "symbol": "CHF"},
            {"currency_code": "ZAR", "currency_name": "South African Rand", "symbol": "R"},
        ]

        for currency in currencies:
            obj, created = Currency.objects.update_or_create(
                currency_code=currency["currency_code"],
                defaults={
                    "currency_name": currency["currency_name"],
                    "symbol": currency["symbol"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {currency['currency_code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {currency['currency_code']}"))

        self.stdout.write(self.style.SUCCESS("✅ Default currencies seeded successfully."))
