"""_summary_
Payement methods seeding script for the RentSafe project.
This script creates default payment methods used in the application.
It is intended to be run once during the initial setup of the application.
"""
from django.core.management.base import BaseCommand
from apps.accounting.models.models import PaymentMethod 

class Command(BaseCommand):
    """Command to seed default payment methods for RentSafe application."""
    help = "Seed default payment methods for RentSafe application."

    def handle(self, *args, **kwargs):
        # Define the default payment methods
        payment_methods = [
            "CASH USD",
            "SWIPE USD",
            "SWIPE ZIG",
            "BANK TRF USD",
            "BANK TRF ZIG",
            "ECOCASH USD",
            "ECOCASH ZIG"
        ]
        

        # Create or update each payment method
        for method in payment_methods:
            PaymentMethod.objects.get_or_create(payment_method_name=method)

        self.stdout.write(self.style.SUCCESS("Default payment methods seeded successfully."))